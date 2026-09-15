import streamlit as st
import chess

st.set_page_config(
    page_title="My Chess",
    page_icon="♟️",
    layout="centered"
)

st.title("♟️ My Chess")

# 게임 초기화
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

board = st.session_state.board

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.header("게임")

    if st.button("🔄 새 게임", use_container_width=True):
        st.session_state.board = chess.Board()
        st.rerun()

    if st.button("↩️ 한 수 되돌리기", use_container_width=True):
        if board.move_stack:
            board.pop()
            st.rerun()

    st.divider()

    st.write("### 게임 상태")

    if board.is_checkmate():
        winner = "흑" if board.turn == chess.WHITE else "백"
        st.error(f"체크메이트! {winner} 승리")
    elif board.is_stalemate():
        st.warning("스테일메이트!")
    elif board.is_check():
        st.warning("체크!")
    else:
        turn = "백" if board.turn == chess.WHITE else "흑"
        st.info(f"{turn} 차례")

# -----------------------------
# 체스판
# -----------------------------

piece_symbols = {
    chess.PAWN: "♟",
    chess.KNIGHT: "♞",
    chess.BISHOP: "♝",
    chess.ROOK: "♜",
    chess.QUEEN: "♛",
    chess.KING: "♚",
}

white_symbols = {
    chess.PAWN: "♙",
    chess.KNIGHT: "♘",
    chess.BISHOP: "♗",
    chess.ROOK: "♖",
    chess.QUEEN: "♕",
    chess.KING: "♔",
}

# 선택된 칸
if "selected_square" not in st.session_state:
    st.session_state.selected_square = None

selected = st.session_state.selected_square

# 체스판 표시
files = "abcdefgh"

for rank in range(7, -1, -1):
    cols = st.columns(8)

    for file_index in range(8):
        square = chess.square(file_index, rank)

        piece = board.piece_at(square)

        is_dark = (file_index + rank) % 2 == 1

        if is_dark:
            color = "#769656"
        else:
            color = "#eeeed2"

        # 선택된 칸
        if square == selected:
            color = "#f6f669"

        piece_text = ""

        if piece:
            if piece.color == chess.WHITE:
                piece_text = white_symbols[piece.piece_type]
            else:
                piece_text = piece_symbols[piece.piece_type]

        button_label = piece_text if piece_text else " "

        clicked = cols[file_index].button(
            button_label,
            key=f"square_{square}",
            use_container_width=True
        )

        if clicked:

            # 아무것도 선택하지 않은 상태
            if selected is None:

                piece = board.piece_at(square)

                if piece and piece.color == board.turn:
                    st.session_state.selected_square = square
                    st.rerun()

            else:

                move = chess.Move(selected, square)

                # 프로모션 처리
                if (
                    board.piece_at(selected)
                    and board.piece_at(selected).piece_type == chess.PAWN
                    and chess.square_rank(square) in [0, 7]
                ):
                    move = chess.Move(
                        selected,
                        square,
                        promotion=chess.QUEEN
                    )

                if move in board.legal_moves:
                    board.push(move)

                st.session_state.selected_square = None
                st.rerun()

# -----------------------------
# 기보
# -----------------------------

st.divider()

st.subheader("📜 기보")

if board.move_stack:
    temp_board = chess.Board()
    moves = []

    for move in board.move_stack:
        san = temp_board.san(move)
        moves.append(san)
        temp_board.push(move)

    for i in range(0, len(moves), 2):
        move_number = i // 2 + 1
        white_move = moves[i]

        if i + 1 < len(moves):
            black_move = moves[i + 1]
            st.write(f"**{move_number}.** {white_move} {black_move}")
        else:
            st.write(f"**{move_number}.** {white_move}")
else:
    st.write("아직 진행된 수가 없습니다.")
