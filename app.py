import streamlit as st
import chess


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="My Chess",
    page_icon="♟",
    layout="centered"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

/* -------------------------------------------------------
   전체 화면
------------------------------------------------------- */

.block-container {
    max-width: 720px !important;
    padding-top: 25px !important;
    padding-bottom: 40px !important;
}


/* -------------------------------------------------------
   제목
------------------------------------------------------- */

h1 {
    text-align: center;
}


/* -------------------------------------------------------
   체스판 바깥 테두리
------------------------------------------------------- */

.chess-board-wrapper {
    max-width: 650px;
    margin: 20px auto;
    padding: 8px;
    background: #3a2925;
    border-radius: 10px;
    box-shadow:
        0 10px 25px rgba(0, 0, 0, 0.25);
}


/* -------------------------------------------------------
   Streamlit columns
------------------------------------------------------- */

div[data-testid="column"] {
    padding: 0 !important;
}


/* -------------------------------------------------------
   체스 칸
------------------------------------------------------- */

/*
   Streamlit 버튼을 체스판의 한 칸으로 사용합니다.
*/

div[data-testid="stButton"] {
    margin: 0 !important;
    padding: 0 !important;
}


/* 버튼 기본 모양 */

div[data-testid="stButton"] > button {
    width: 100% !important;

    min-height: 72px !important;

    padding: 0 !important;
    margin: 0 !important;

    border-radius: 0 !important;
    border: none !important;

    font-family:
        "Segoe UI Symbol",
        "Noto Sans Symbols 2",
        "Arial Unicode MS",
        sans-serif !important;

    font-size: 48px !important;
    line-height: 1 !important;

    box-shadow: none !important;

    transition:
        filter 0.1s ease,
        transform 0.1s ease !important;
}


/* 버튼 hover */

div[data-testid="stButton"] > button:hover {
    filter: brightness(1.08) !important;
    transform: scale(0.97);
}


/* 버튼 내부 */

div[data-testid="stButton"] > button p {
    margin: 0 !important;
    padding: 0 !important;
}


/* -------------------------------------------------------
   흰색 말
------------------------------------------------------- */

.white-piece {
    color: #ffffff;
    text-shadow:
        -1px -1px 1px #222222,
         1px -1px 1px #222222,
        -1px  1px 1px #222222,
         1px  1px 1px #222222,
         0px 3px 5px rgba(0, 0, 0, 0.6);
}


/* -------------------------------------------------------
   검은색 말
------------------------------------------------------- */

.black-piece {
    color: #111111;
    text-shadow:
        0px 2px 3px rgba(255, 255, 255, 0.25),
        0px 4px 5px rgba(0, 0, 0, 0.6);
}


/* -------------------------------------------------------
   모바일
------------------------------------------------------- */

@media (max-width: 600px) {

    .block-container {
        padding-left: 6px !important;
        padding-right: 6px !important;
    }

    .chess-board-wrapper {
        padding: 5px;
    }

    div[data-testid="stButton"] > button {
        min-height: 43px !important;
        font-size: 31px !important;
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
# 게임 초기화
# =========================================================

if "board" not in st.session_state:
    st.session_state.board = chess.Board()

if "selected_square" not in st.session_state:
    st.session_state.selected_square = None


board = st.session_state.board
selected_square = st.session_state.selected_square


# =========================================================
# 제목
# =========================================================

st.title("♟ My Chess")


# =========================================================
# 현재 게임 상태
# =========================================================

if board.is_checkmate():

    winner = "흑" if board.turn == chess.WHITE else "백"

    st.error(
        f"♔ 체크메이트! **{winner}의 승리입니다!**"
    )

elif board.is_stalemate():

    st.warning(
        "무승부입니다. 스테일메이트!"
    )

elif board.is_insufficient_material():

    st.warning(
        "무승부입니다. 기물 부족!"
    )

elif board.is_check():

    turn = "백" if board.turn == chess.WHITE else "흑"

    st.warning(
        f"⚠️ {turn}의 왕이 체크 상태입니다."
    )

else:

    turn = "백" if board.turn == chess.WHITE else "흑"

    st.info(
        f"현재 차례: **{turn}**
    )


# =========================================================
# 새 게임 / 되돌리기
# =========================================================

button_col1, button_col2 = st.columns(2)


with button_col1:

    if st.button(
        "🔄 새 게임",
        use_container_width=True
    ):

        st.session_state.board = chess.Board()
        st.session_state.selected_square = None

        st.rerun()


with button_col2:

    if st.button(
        "↩️ 한 수 되돌리기",
        use_container_width=True
    ):

        if board.move_stack:

            board.pop()

            st.session_state.selected_square = None

            st.rerun()


# =========================================================
# 선택된 말의 이동 가능 위치 계산
# =========================================================

legal_targets = set()

capture_targets = set()


if selected_square is not None:

    for move in board.legal_moves:

        if move.from_square == selected_square:

            legal_targets.add(move.to_square)

            if board.is_capture(move):

                capture_targets.add(move.to_square)


# =========================================================
# 체스판
# =========================================================

st.markdown(
    '<div class="chess-board-wrapper">',
    unsafe_allow_html=True
)


# =========================================================
# 8 x 8
# =========================================================

for rank in range(7, -1, -1):

    cols = st.columns(8, gap=None)

    for file_index in range(8):

        square = chess.square(
            file_index,
            rank
        )

        piece = board.piece_at(square)


        # -------------------------------------------------
        # 칸 색상
        # -------------------------------------------------

        if (file_index + rank) % 2 == 0:

            # 밝은 칸
            base_color = "#F0D9B5"

        else:

            # 어두운 칸
            base_color = "#B58863"


        # -------------------------------------------------
        # 선택된 칸
        # -------------------------------------------------

        if square == selected_square:

            base_color = "#F6E652"


        # -------------------------------------------------
        # 이동 가능한 칸
        # -------------------------------------------------

        if square in legal_targets:

            if square in capture_targets:

                # 잡을 수 있는 칸
                base_color = "#D97878"

            else:

                # 이동 가능한 칸
                base_color = "#9BCB77"


        # -------------------------------------------------
        # 체스 말
        # -------------------------------------------------

        if piece is None:

            symbol = " "

        else:

            if piece.color == chess.WHITE:

                symbol = WHITE_PIECES[
                    piece.piece_type
                ]

            else:

                symbol = BLACK_PIECES[
                    piece.piece_type
                ]


        # -------------------------------------------------
        # 글자 색
        # -------------------------------------------------

        if piece:

            if piece.color == chess.WHITE:

                text_color = "#FFFFFF"

                text_shadow = """
                    -1px -1px 1px #222,
                     1px -1px 1px #222,
                    -1px  1px 1px #222,
                     1px  1px 1px #222,
                     0 3px 5px rgba(0,0,0,0.6)
                """

            else:

                text_color = "#111111"

                text_shadow = """
                    0 2px 3px rgba(255,255,255,0.25),
                    0 4px 5px rgba(0,0,0,0.6)
                """

        else:

            text_color = base_color
            text_shadow = "none"


        # -------------------------------------------------
        # 칸 배경을 버튼에 적용
        #
        # Streamlit 버튼은 직접 CSS 색상을 넣기 어렵기
        # 때문에 버튼 바로 앞에서 스타일을 지정합니다.
        # -------------------------------------------------

        unique_class = (
            f"board_square_{rank}_{file_index}"
        )


        st.markdown(
            f"""
            <style>

            .{unique_class} + div[data-testid="stButton"] > button {{
                background-color: {base_color} !important;
                color: {text_color} !important;

                text-shadow: {text_shadow} !important;

                border: none !important;
                border-radius: 0 !important;

                min-height: 72px !important;

                font-size: 48px !important;
                line-height: 1 !important;

                padding: 0 !important;
                margin: 0 !important;
            }}

            .{unique_class} + div[data-testid="stButton"] > button:hover {{
                background-color: {base_color} !important;
                filter: brightness(1.08) !important;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # 빈 HTML 요소
        # -------------------------------------------------

        with cols[file_index]:

            st.markdown(
                f'<div class="{unique_class}"></div>',
                unsafe_allow_html=True
            )


            # -------------------------------------------------
            # 버튼
            # -------------------------------------------------

            clicked = st.button(
                symbol,
                key=f"square_{square}",
                use_container_width=True
            )


            # -------------------------------------------------
            # 클릭 처리
            # -------------------------------------------------

            if clicked:

                # =========================================
                # 선택된 말이 없는 경우
                # =========================================

                if selected_square is None:

                    if (
                        piece is not None
                        and
                        piece.color == board.turn
                    ):

                        st.session_state.selected_square = square

                        st.rerun()


                # =========================================
                # 이미 말을 선택한 경우
                # =========================================

                else:

                    move = chess.Move(
                        selected_square,
                        square
                    )


                    # =====================================
                    # 폰 프로모션
                    # =====================================

                    selected_piece = board.piece_at(
                        selected_square
                    )

                    if (
                        selected_piece is not None
                        and
                        selected_piece.piece_type
                        == chess.PAWN
                        and
                        chess.square_rank(square)
                        in [0, 7]
                    ):

                        # 기본적으로 퀸으로 승격
                        move = chess.Move(
                            selected_square,
                            square,
                            promotion=chess.QUEEN
                        )


                    # =====================================
                    # 합법적인 이동
                    # =====================================

                    if move in board.legal_moves:

                        board.push(move)

                        st.session_state.selected_square = None

                        st.rerun()


                    # =====================================
                    # 다른 내 말을 클릭
                    # =====================================

                    elif (
                        piece is not None
                        and
                        piece.color == board.turn
                    ):

                        st.session_state.selected_square = square

                        st.rerun()


                    # =====================================
                    # 선택 취소
                    # =====================================

                    else:

                        st.session_state.selected_square = None

                        st.rerun()


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 현재 선택한 말 정보
# =========================================================

if selected_square is not None:

    piece = board.piece_at(selected_square)

    if piece:

        if piece.color == chess.WHITE:

            color_name = "백"

        else:

            color_name = "흑"


        piece_names = {
            chess.PAWN: "폰",
            chess.KNIGHT: "나이트",
            chess.BISHOP: "비숍",
            chess.ROOK: "룩",
            chess.QUEEN: "퀸",
            chess.KING: "킹",
        }


        st.caption(
            f"선택: {color_name} "
            f"{piece_names[piece.piece_type]}"
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

    st.caption(
        "아직 진행된 수가 없습니다."
    )


# =========================================================
# 게임 종료 안내
# =========================================================

if board.is_game_over():

    st.divider()

    if board.is_checkmate():

        winner = "흑" if board.turn == chess.WHITE else "백"

        st.success(
            f"🏆 게임 종료 — {winner} 승리!"
        )

    elif board.is_stalemate():

        st.info(
            "🤝 게임 종료 — 무승부"
        )

    elif board.is_insufficient_material():

        st.info(
            "🤝 게임 종료 — 무승부"
        )
