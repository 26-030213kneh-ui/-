import streamlit as st
import chess

# =========================================================
# 페이지 설정
# =========================================================

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

/* 전체 페이지 */
.block-container {
    max-width: 760px !important;
    padding-top: 25px !important;
}


/* ================================
   체스판
================================ */

.chess-container {
    width: 100%;
    max-width: 640px;
    margin: 25px auto 10px auto;
    padding: 8px;
    background: #3b2f2f;
    border-radius: 10px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}


/* ================================
   Streamlit column
================================ */

div[data-testid="column"] {
    padding: 0 !important;
}


/* ================================
   체스 칸 버튼
================================ */

/*
   모든 Streamlit 버튼을 체스판 버튼으로 사용
*/

.chess-cell button {
    width: 100% !important;
    height: 100% !important;

    min-height: 70px !important;

    padding: 0 !important;
    margin: 0 !important;

    border: none !important;
    border-radius: 0 !important;

    font-size: 48px !important;
    line-height: 1 !important;

    font-family:
        "Segoe UI Symbol",
        "Noto Sans Symbols 2",
        "Arial Unicode MS",
        sans-serif !important;

    transition: 0.12s ease !important;
}


/* 버튼 hover */
.chess-cell button:hover {
    transform: scale(0.97);
    filter: brightness(1.08);
}


/* 버튼 안의 텍스트 */
.chess-cell button p {
    margin: 0 !important;
    padding: 0 !important;
}


/* ================================
   좌표
================================ */

.coordinate {
    font-size: 11px;
    font-weight: bold;
    opacity: 0.6;
}


/* ================================
   모바일
================================ */

@media (max-width: 600px) {

    .block-container {
        padding-left: 8px !important;
        padding-right: 8px !important;
    }

    .chess-container {
        padding: 5px;
    }

    .chess-cell button {
        min-height: 43px !important;
        font-size: 32px !important;
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
# 현재 상태
# =========================================================

if board.is_checkmate():

    winner = "흑" if board.turn == chess.WHITE else "백"

    st.error(
        f"♚ 체크메이트! **{winner} 승리!**"
    )

elif board.is_stalemate():

    st.warning("무승부 — 스테일메이트")

elif board.is_check():

    turn = "백" if board.turn == chess.WHITE else "흑"

    st.warning(
        f"⚠️ {turn}의 왕이 체크 상태입니다."
    )

else:

    turn = "백" if board.turn == chess.WHITE else "흑"

    st.info(
        f"현재 차례: **{turn}**"
    )


# =========================================================
# 새 게임 / 되돌리기
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
# 이동 가능한 칸 계산
# =========================================================

legal_targets = set()

if selected is not None:

    for move in board.legal_moves:

        if move.from_square == selected:

            legal_targets.add(move.to_square)


# =========================================================
# 체스판 시작
# =========================================================

st.markdown(
    '<div class="chess-container">',
    unsafe_allow_html=True
)


files = "abcdefgh"


# =========================================================
# 8 x 8 체스판
# =========================================================

for rank in range(7, -1, -1):

    columns = st.columns(8, gap="small")

    for file_index in range(8):

        square = chess.square(
            file_index,
            rank
        )

        piece = board.piece_at(square)


        # ---------------------------------------------
        # 칸 색깔
        # ---------------------------------------------

        if (file_index + rank) % 2 == 0:

            square_color = "#F0D9B5"

        else:

            square_color = "#B58863"


        # ---------------------------------------------
        # 선택된 칸
        # ---------------------------------------------

        if square == selected:

            square_color = "#F6E652"


        # ---------------------------------------------
        # 이동 가능한 칸
        # ---------------------------------------------

        is_legal_target = square in legal_targets


        # ---------------------------------------------
        # 말
        # ---------------------------------------------

        if piece:

            if piece.color == chess.WHITE:

                symbol = WHITE_PIECES[
                    piece.piece_type
                ]

            else:

                symbol = BLACK_PIECES[
                    piece.piece_type
                ]

        else:

            symbol = " "


        # ---------------------------------------------
        # 버튼
        # ---------------------------------------------

        with columns[file_index]:

            st.markdown(
                f"""
                <style>
                div[data-testid="stButton"]
                button[kind="secondary"] {{
                    background-color: {square_color} !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="chess-cell">',
                unsafe_allow_html=True
            )

            clicked = st.button(
                symbol,
                key=f"chess_square_{square}",
                use_container_width=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


            # -----------------------------------------
            # 클릭 처리
            # -----------------------------------------

            if clicked:

                # 선택된 말이 없는 경우
                if selected is None:

                    if (
                        piece
                        and piece.color == board.turn
                    ):

                        st.session_state.selected_square = square

                        st.rerun()


                # 이미 말을 선택한 경우
                else:

                    move = chess.Move(
                        selected,
                        square
                    )


                    # ---------------------------------
                    # 폰 프로모션
                    # ---------------------------------

                    selected_piece = board.piece_at(
                        selected
                    )

                    if (
                        selected_piece
                        and
                        selected_piece.piece_type
                        == chess.PAWN
                        and
                        chess.square_rank(square)
                        in [0, 7]
                    ):

                        move = chess.Move(
                            selected,
                            square,
                            promotion=chess.QUEEN
                        )


                    # ---------------------------------
                    # 합법적인 이동
                    # ---------------------------------

                    if move in board.legal_moves:

                        board.push(move)

                        st.session_state.selected_square = None

                        st.rerun()


                    # ---------------------------------
                    # 다른 내 말 선택
                    # ---------------------------------

                    elif (
                        piece
                        and piece.color == board.turn
                    ):

                        st.session_state.selected_square = square

                        st.rerun()


                    # ---------------------------------
                    # 선택 취소
                    # ---------------------------------

                    else:

                        st.session_state.selected_square = None

                        st.rerun()


st.markdown(
    '</div>',
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

    st.write(
        "아직 진행된 수가 없습니다."
    )
