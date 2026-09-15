import streamlit as st
import chess

st.set_page_config(
    page_title="My Chess",
    page_icon="♟️",
    layout="centered"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.main .block-container {
    max-width: 850px;
    padding-top: 2rem;
}

/* 체스판 */
.chess-board {
    width: 100%;
    max-width: 720px;
    margin: 20px auto;
    border: 10px solid #3b2f2f;
    border-radius: 8px;
    overflow: hidden;
    box-shadow:
        0 12px 30px rgba(0,0,0,0.35),
        inset 0 0 0 2px rgba(255,255,255,0.15);
}

/* 한 줄 */
.chess-row {
    display: flex;
    width: 100%;
}

/* 한 칸 */
.chess-square {
    width: 12.5%;
    aspect-ratio: 1 / 1;

    display: flex;
    align-items: center;
    justify-content: center;

    position: relative;

    cursor: pointer;

    font-family:
        "Arial Unicode MS",
        "Noto Sans Symbols 2",
        "Segoe UI Symbol",
        sans-serif;

    transition: filter 0.12s ease;
}

/* 밝은 칸 */
.light-square {
    background-color: #f0d9b5;
}

/* 어두운 칸 */
.dark-square {
    background-color: #b58863;
}

/* 마우스를 올렸을 때 */
.chess-square:hover {
    filter: brightness(1.12);
}

/* 체스 말 */
.chess-piece {
    font-size: clamp(42px, 7vw, 72px);
    line-height: 1;

    user-select: none;

    filter:
        drop-shadow(0px 3px 2px rgba(0,0,0,0.45));

    transform: translateY(-2px);

    z-index: 2;
}

/* 흰색 말 */
.white-piece {
    color: #ffffff;

    text-shadow:
        -1px -1px 0 #222,
         1px -1px 0 #222,
        -1px  1px 0 #222,
         1px  1px 0 #222,
         0px 3px 5px rgba(0,0,0,0.5);
}

/* 검은색 말 */
.black-piece {
    color: #171717;

    text-shadow:
        0px 2px 3px rgba(255,255,255,0.25),
        0px 4px 6px rgba(0,0,0,0.6);
}

/* 선택된 칸 */
.selected-square {
    background-color: #f7ec55 !important;
    box-shadow:
        inset 0 0 0 5px rgba(255, 193, 7, 0.8);
}

/* 이동 가능한 칸 */
.legal-square::after {
    content: "";
    position: absolute;

    width: 22%;
    height: 22%;

    background-color: rgba(30, 130, 76, 0.75);

    border-radius: 50%;

    z-index: 1;
}

/* 말을 잡을 수 있는 칸 */
.capture-square::after {
    content: "";

    position: absolute;

    width: 72%;
    height: 72%;

    border: 5px solid rgba(190, 40, 40, 0.75);

    border-radius: 50%;

    z-index: 1;
}

/* 좌표 */
.board-coordinate {
    position: absolute;

    font-size: 12px;
    font-weight: bold;

    opacity: 0.65;

    z-index: 3;
}

.rank-coordinate {
    top: 3px;
    left: 5px;
}

.file-coordinate {
    bottom: 3px;
    right: 5px;
}

/* 모바일 */
@media (max-width: 600px) {

    .main .block-container {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }

    .chess-board {
        border-width: 6px;
    }

    .chess-piece {
        font-size: clamp(34px, 11vw, 52px);
    }

    .board-coordinate {
        font-size: 9px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 체스 말
# =========================================================

WHITE_PIECES = {
    chess.PAWN: "♙",
    chess.KNIGHT: "♘",
    chess.BISHOP: "♗",
    chess.ROOK: "♖",
    chess.QUEEN: "♕",
    chess.KING: "♔",
}

BLACK_PIECES = {
    chess.PAWN: "♟",
    chess.KNIGHT: "♞",
    chess.BISHOP: "♝",
    chess.ROOK: "♜",
    chess.QUEEN: "♛",
    chess.KING: "♚",
}


# =========================================================
# 게임 상태
# =========================================================

if "board" not in st.session_state:
    st.session_state.board = chess.Board()

if "selected_square" not in st.session_state:
    st.session_state.selected_square = None

board = st.session_state.board
selected = st.session_state.selected_square


# =========================================================
# 제목
# =========================================================

st.title("♟️ My Chess")


# =========================================================
# 게임 상태
# =========================================================

if board.is_checkmate():

    winner = "흑" if board.turn == chess.WHITE else "백"
    st.error(f"♔ 체크메이트! {winner} 승리!")

elif board.is_stalemate():

    st.warning("무승부 — 스테일메이트")

elif board.is_check():

    turn = "백" if board.turn == chess.WHITE else "흑"
    st.warning(f"⚠️ {turn}의 왕이 체크 상태입니다.")

else:

    turn = "백" if board.turn == chess.WHITE else "흑"
    st.info(f"현재 차례: **{turn}**")


# =========================================================
# 버튼
# =========================================================

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🔄 새 게임",
        use_container_width=True
    ):
        st.session_state.board = chess.Board()
        st.session_state.selected_square = None
        st.rerun()


with col2:

    if st.button(
        "↩️ 한 수 되돌리기",
        use_container_width=True
    ):

        if board.move_stack:

            board.pop()

            st.session_state.selected_square = None

            st.rerun()


# =========================================================
# 합법적인 이동 계산
# =========================================================

legal_targets = set()

if selected is not None:

    for move in board.legal_moves:

        if move.from_square == selected:
            legal_targets.add(move.to_square)


# =========================================================
# 체스판
# =========================================================

st.markdown(
    '<div class="chess-board">',
    unsafe_allow_html=True
)

files = "abcdefgh"

for rank in range(7, -1, -1):

    st.markdown(
        '<div class="chess-row">',
        unsafe_allow_html=True
    )

    for file_index in range(8):

        square = chess.square(
            file_index,
            rank
        )

        piece = board.piece_at(square)

        # ---------------------------------------------
        # 색
        # ---------------------------------------------

        if (file_index + rank) % 2 == 0:

            square_color = "light-square"

        else:

            square_color = "dark-square"


        # ---------------------------------------------
        # 선택
        # ---------------------------------------------

        if square == selected:

            square_color += " selected-square"


        # ---------------------------------------------
        # 이동 가능
        # ---------------------------------------------

        if square in legal_targets:

            if piece is None:

                square_color += " legal-square"

            else:

                square_color += " capture-square"


        # ---------------------------------------------
        # 말
        # ---------------------------------------------

        piece_html = ""

        if piece:

            if piece.color == chess.WHITE:

                symbol = WHITE_PIECES[piece.piece_type]

                piece_class = "white-piece"

            else:

                symbol = BLACK_PIECES[piece.piece_type]

                piece_class = "black-piece"


            piece_html = f"""
                <div class="chess-piece {piece_class}">
                    {symbol}
                </div>
            """


        # ---------------------------------------------
        # 좌표
        # ---------------------------------------------

        coordinate_html = ""

        if file_index == 0:

            coordinate_html += f"""
                <span class="board-coordinate rank-coordinate">
                    {rank + 1}
                </span>
            """

        if rank == 0:

            coordinate_html += f"""
                <span class="board-coordinate file-coordinate">
                    {files[file_index]}
                </span>
            """


        # ---------------------------------------------
        # 실제 버튼
        # ---------------------------------------------

        button_key = f"square_{square}"

        if st.button(
            piece_html if piece_html else " ",
            key=button_key,
            use_container_width=True
        ):

            # 아무것도 선택되지 않은 경우
            if selected is None:

                if piece and piece.color == board.turn:

                    st.session_state.selected_square = square

                    st.rerun()


            # 이미 말을 선택한 경우
            else:

                move = chess.Move(
                    selected,
                    square
                )

                # 폰 프로모션
                selected_piece = board.piece_at(selected)

                if (
                    selected_piece
                    and selected_piece.piece_type == chess.PAWN
                    and chess.square_rank(square) in [0, 7]
                ):

                    move = chess.Move(
                        selected,
                        square,
                        promotion=chess.QUEEN
                    )


                # 합법적인 이동
                if move in board.legal_moves:

                    board.push(move)

                    st.session_state.selected_square = None

                    st.rerun()

                # 다른 내 말을 선택
                elif piece and piece.color == board.turn:

                    st.session_state.selected_square = square

                    st.rerun()

                else:

                    st.session_state.selected_square = None

                    st.rerun()


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# 기보
# =========================================================

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

            st.write(
                f"**{move_number}.** "
                f"{white_move} "
                f"{black_move}"
            )

        else:

            st.write(
                f"**{move_number}.** "
                f"{white_move}"
            )

else:

    st.write("아직 진행된 수가 없습니다.")
