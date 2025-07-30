import json

from fastapi import APIRouter
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from starlette.websockets import WebSocketDisconnect

from db.models import Game, Player, Question, Answer
from db.sessions import SessionDep

#
socket = APIRouter()
#
templates = Jinja2Templates(directory='templates')


@socket.get("/join/{game_code}")
async def join_game(request: Request, game_code: str):
    return templates.TemplateResponse("join.html", {"request": request, "game_code": game_code})


@socket.get('/kahoot/')
async def home(request: Request, game_code: str, nickname: str):
    return templates.TemplateResponse("kahoot.html", {"request": request, 'game_code': game_code, 'nickname': nickname})


class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        self.rooms.setdefault(room_id, []).append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        self.rooms[room_id].remove(websocket)
        if not self.rooms[room_id]:
            del self.rooms[room_id]

    async def broadcast(self, room_id: str, message: str):
        for ws in self.rooms.get(room_id, []):
            await ws.send_text(message)


manager = ConnectionManager()


@socket.websocket("/ws/{room_id}/{nickname}/")
async def websocket_endpoint(session: SessionDep, websocket: WebSocket, room_id: str, nickname: str):
    game = await Game.get(session, Game.code, room_id)
    print(game)
    if not game:
        await websocket.accept()
        await websocket.send_text("❌ Game not found.")
        await websocket.close(code=1008)
        return
    player = await Player.create(session, name=nickname, game_id=game.id)
    await manager.connect(room_id, websocket)
    await manager.broadcast(room_id, f"{nickname} joined the game 🎮")
    try:
        while True:
            data = await websocket.receive_text()
            await Answer.create(session, text=data, player_id=player.id)
            question = await Question.get(session, Question.correct_answer, data)
            if question:
                await Player.update(session, player.id, balance=question.ball)
            top_players = await Player.query(session, select(Player).
                                             where(Player.game_id == game.id).order_by(Player.balance.desc()))
            leaderboard_data = {
                "type": "leaderboard",
                "players": [{"name": p.name, "score": p.balance or 0} for p in top_players[:5]]
            }
            await manager.broadcast(room_id, json.dumps(leaderboard_data))
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
        await manager.broadcast(room_id, f"{nickname} left ❌")
