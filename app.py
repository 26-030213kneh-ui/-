import streamlit as st
import chess


# ============================================================
# 페이지 설정
# ============================================================

st.set_page_config(
    page_title="My Chess",
    page_icon="♟",
    layout="centered",
)


# ============================================================
# 체스 말
# ============================================================

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


PIECE_NAMES = {
    chess.PAWN: "폰",
    chess.KNIGHT: "나이트",
    chess.BISHOP: "비숍",
    chess.ROOK: "룩",
    chess.QUEEN: "퀸",
    chess.KING: "킹",
}


FILES = "abcdefgh"


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       전체 페이지
    ===================================================== */

    .block-container {
        max-width: 720px !important;
        padding-top: 25px !important;
        padding-bottom: 40px !important;
    }


    /* =====================================================
       제목
    ===================================================== */

    h1 {
        text-align: center;
        margin-bottom: 15px;
    }


    /* =====================================================
       체스판 바깥
    ===================================================== */

    .chess-frame {
        width: 100%;
        max-width: 640px;
        margin: 20px auto;
        padding: 8px;

        background: #382b27;

        border-radius: 12px;

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.28),
            inset 0 0 0 2px rgba(255, 255, 255, 0.08);
    }


    /* =====================================================
       체스판 행
    ===================================================== */

    [class*="st-key-boardrow"] {
        padding: 0 !important;
        margin: 0 !important;
    }


    /* =====================================================
       체스판의 8개 column
    ===================================================== */

    [class*="st-key-boardrow"] [data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
    }


    /* =====================================================
       체스판 버튼
    ===================================================== */

    [class*="st-key-boardrow"]
    [data-testid="column"]
    [data-testid="stButton"] {

        margin: 0 !important;
        padding: 0 !important;
    }


    [class*="st-key-boardrow"]
    [data-testid="column"]
    [data-testid="stButton"] > button {

        width: 100% !important;

        min-height: 76px !important;

        height: 76px !important;

        padding: 0 !important;
        margin: 0 !important;

        border: none !important;
        border-radius: 0 !important;

        font-family:
            "Segoe UI Symbol",
            "Noto Sans Symbols 2",
            "Arial Unicode MS",
            sans-serif !important;

        font-size: 50px !important;

        line-height: 1 !important;

        box-shadow: none !important;

        transition:
            filter 0.12s ease,
            transform 0.08s ease !important;
    }


    /* =====================================================
       버튼 안쪽 글자
    ===================================================== */

    [class*="st-key-boardrow"]
    [data-testid="column"]
    [data-testid="stButton"] button p {

        margin: 0 !important;
        padding: 0 !important;

        line-height: 1 !important;
    }


    /* =====================================================
       마우스 올렸을 때
    ===================================================== */

    [class*="st-key-boardrow"]
    [data-testid="column"]
    [data-testid="stButton"] > button:hover {

        filter: brightness(1.08) !important;

        transform: scale(0.97);
    }


    /* =====================================================
       모바일
    ===================================================== */

    @media (max-width: 600px) {

        .block-container {
            padding-left: 6px !important;
            padding-right: 6px !important;
        }

        .chess-frame {
            padding: 5px;
        }

        [class*="st-key-boardrow"]
        [data-testid="stButton"] > button {

            min-height: 43px !important;
            height: 43px !important;

            font-size: 31px !important;
        }
    }


    /* =====================================================
       기보
    ===================================================== */

    .move-list {
        background: #f7f7f7;
        padding: 12px 16px;
        border-radius: 8px;
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 게임 상태 초기화
# ============================================================

if "board" not in st.session_state:
    st.session_state.board = chess.Board()

if "selected_square" not in st.session_state:
    st.session_state.selected_square = None

if "pending_promotion" not in st.session_state:
    st.session_state.pending_promotion = None


board = st.session_state.board
selected_square = st.session_state.selected_square
pending_promotion = st.session_state.pending_promotion


# ============================================================
# 함수
# ============================================================

def reset_game():
    """새 게임 시작"""

    st.session_state.board = chess.Board()
    st.session_state.selected_square = None
    st.session_state.pending_promotion = None


def undo_move():
    """한 수 되돌리기"""

    if st.session_state.pending_promotion is not None:

        st.session_state.pending_promotion = None
        st.session_state.selected_square = None

        return

    if st.session_state.board.move_stack:

        st.session_state.board.pop()

        st.session_state.selected_square = None
        st.session_state.pending_promotion = None


def piece_symbol(piece):
    """체스 말 기호 반환"""

    if piece is None:
        return " "

    if piece.color == chess.WHITE:
        return WHITE_PIECES[piece.piece_type]

    return BLACK_PIECES[piece.piece_type]


def square_name(square):
    """체스판 좌표 반환"""

    return chess.square_name(square)


def make_move(from_square, to_square, promotion=None):
    """실제 수를 둔다"""

    move = chess.Move(
        from_square,
        to_square,
        promotion=promotion,
    )

    if move in board.legal_moves:

        board.push(move)

        st.session_state.selected_square = None
        st.session_state.pending_promotion = None

        return True

    return False


# ============================================================
# 제목
# ============================================================

st.title("♟ My Chess")


# ============================================================
# 현재 상태
# ============================================================

if board.is_checkmate():

    winner = "흑" if board.turn == chess.WHITE else "백"

    st.error(
        f"♚ 체크메이트! **{winner}의 승리입니다!**"
    )

elif board.is_stalemate():

    st.warning(
        "🤝 스테일메이트 — 무승부입니다."
    )

elif board.is_insufficient_material():

    st.warning(
        "🤝 기물 부족 — 무승부입니다."
    )

elif board.is_check():

    turn = "백" if board.turn == chess.WHITE else "흑"

    st.warning(
        f"⚠️ {turn}의 왕이 체크 상태입니다!"
    )

else:

    turn = "백" if board.turn == chess.WHITE else "흑"

    st.info(
        f"현재 차례: **{turn}**"
    )


# ============================================================
# 새 게임 / 되돌리기
# ============================================================

button1, button2 = st.columns(2)

with button1:

    if st.button(
        "🔄 새 게임",
        width="stretch",
    ):

        reset_game()
        st.rerun()


with button2:

    if st.button(
        "↩️ 한 수 되돌리기",
        width="stretch",
    ):

        undo_move()
        st.rerun()


# ============================================================
# 선택된 말의 이동 가능 칸
# ============================================================

legal_targets = set()
capture_targets = set()


if selected_square is not None:

    for move in board.legal_moves:

        if move.from_square == selected_square:

            legal_targets.add(move.to_square)

            if board.is_capture(move):

                capture_targets.add(move.to_square)


# ============================================================
# 체크 상태인 왕
# ============================================================

checked_king = None

if board.is_check():

    checked_king = board.king(board.turn)


# ============================================================
# 체스판 CSS 생성
# ============================================================

board_css = "<style>\n"


for rank in range(7, -1, -1):

    row_key = f"boardrow{rank}"

    for file_index in range(8):

        square = chess.square(
            file_index,
            rank,
        )

        # ----------------------------------------------------
        # 기본 칸 색상
        # ----------------------------------------------------

        if (file_index + rank) % 2 == 0:

            color = "#F0D9B5"

        else:

            color = "#B58863"


        # ----------------------------------------------------
        # 체크 상태인 왕
        # ----------------------------------------------------

        if square == checked_king:

            color = "#E57373"


        # ----------------------------------------------------
        # 선택된 칸
        # ----------------------------------------------------

        if square == selected_square:

            color = "#F4D35E"


        # ----------------------------------------------------
        # 이동 가능한 칸
        # ----------------------------------------------------

        if square in legal_targets:

            if square in capture_targets:

                color = "#D96C6C"

            else:

                color = "#9BCB77"


        # ----------------------------------------------------
        # 말 색상
        # ----------------------------------------------------

        piece = board.piece_at(square)

        if piece is None:

            text_color = "transparent"

            shadow = "none"

        elif piece.color == chess.WHITE:

            text_color = "#FFFFFF"

            shadow = """
                -1px -1px 1px #222222,
                 1px -1px 1px #222222,
                -1px  1px 1px #222222,
                 1px  1px 1px #222222,
                 0 4px 6px rgba(0,0,0,0.55)
            """

        else:

            text_color = "#111111"

            shadow = """
                0 2px 3px rgba(255,255,255,0.25),
                0 4px 6px rgba(0,0,0,0.65)
            """


        # ----------------------------------------------------
        # CSS selector
        # ----------------------------------------------------

        board_css += f"""
        .st-key-{row_key}
        [data-testid="column"]:nth-child({file_index + 1})
        [data-testid="stButton"] > button {{

            background-color: {color} !important;

            color: {text_color} !important;

            text-shadow: {shadow} !important;

            border: none !important;

            border-radius: 0 !important;
        }}

        .st-key-{row_key}
        [data-testid="column"]:nth-child({file_index + 1})
        [data-testid="stButton"] > button:hover {{

            background-color: {color} !important;
        }}
        """


board_css += "</style>"


st.markdown(
    board_css,
    unsafe_allow_html=True,
)


# ============================================================
# 체스판
# ============================================================

st.markdown(
    '<div class="chess-frame">',
    unsafe_allow_html=True,
)


for rank in range(7, -1, -1):

    row_key = f"boardrow{rank}"

    # 각 행을 별도의 CSS 컨테이너로 만듦
    with st.container(
        key=row_key,
    ):

        # 8개 칸
        cols = st.columns(
            8,
            gap=None,
            vertical_alignment="center",
            wrap=False,
        )

        for file_index in range(8):

            square = chess.square(
                file_index,
                rank,
            )

            piece = board.piece_at(square)

            symbol = piece_symbol(piece)


            with cols[file_index]:

                clicked = st.button(
                    symbol,
                    key=f"square_{square}",
                    width="stretch",
                )


                # =================================================
                # 클릭 처리
                # =================================================

                if clicked:

                    # ---------------------------------------------
                    # 승부가 끝난 경우
                    # ---------------------------------------------

                    if board.is_game_over():

                        continue


                    # ---------------------------------------------
                    # 프로모션 선택 중
                    # ---------------------------------------------

                    if pending_promotion is not None:

                        continue


                    # ---------------------------------------------
                    # 아무 말도 선택하지 않은 상태
                    # ---------------------------------------------

                    if selected_square is None:

                        if (
                            piece is not None
                            and
                            piece.color == board.turn
                        ):

                            st.session_state.selected_square = square

                            st.rerun()


                    # ---------------------------------------------
                    # 이미 말을 선택한 상태
                    # ---------------------------------------------

                    else:

                        selected_piece = board.piece_at(
                            selected_square
                        )


                        if selected_piece is None:

                            st.session_state.selected_square = None

                            st.rerun()


                        # -----------------------------------------
                        # 같은 색 말 클릭
                        # -----------------------------------------

                        if (
                            piece is not None
                            and
                            piece.color == board.turn
                        ):

                            st.session_state.selected_square = square

                            st.rerun()


                        # -----------------------------------------
                        # 폰 프로모션
                        # -----------------------------------------

                        is_promotion = (
                            selected_piece is not None
                            and
                            selected_piece.piece_type == chess.PAWN
                            and
                            chess.square_rank(square) in (0, 7)
                        )


                        if is_promotion:

                            test_move = chess.Move(
                                selected_square,
                                square,
                                promotion=chess.QUEEN,
                            )

                            if test_move in board.legal_moves:

                                st.session_state.pending_promotion = (
                                    selected_square,
                                    square,
                                )

                                st.rerun()


                        # -----------------------------------------
                        # 일반 이동
                        # -----------------------------------------

                        else:

                            if make_move(
                                selected_square,
                                square,
                            ):

                                st.rerun()

                            else:

                                # 잘못된 칸을 누르면 선택 취소
                                st.session_state.selected_square = None

                                st.rerun()


st.markdown(
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# 프로모션 선택
# ============================================================

if st.session_state.pending_promotion is not None:

    from_square, to_square = (
        st.session_state.pending_promotion
    )

    st.subheader("♟ 폰 승격")

    st.write(
        "승격할 말을 선택하세요."
    )

    promotion_cols = st.columns(4)

    promotion_options = [
        (chess.QUEEN, "♕ 퀸"),
        (chess.ROOK, "♖ 룩"),
        (chess.BISHOP, "♗ 비숍"),
        (chess.KNIGHT, "♘ 나이트"),
    ]


    for index, (piece_type, label) in enumerate(
        promotion_options
    ):

        with promotion_cols[index]:

            if st.button(
                label,
                key=f"promotion_{piece_type}",
                width="stretch",
            ):

                move = chess.Move(
                    from_square,
                    to_square,
                    promotion=piece_type,
                )

                if move in board.legal_moves:

                    board.push(move)

                st.session_state.selected_square = None
                st.session_state.pending_promotion = None

                st.rerun()


# ============================================================
# 선택된 말 정보
# ============================================================

if (
    st.session_state.selected_square is not None
    and
    st.session_state.pending_promotion is None
):

    selected_piece = board.piece_at(
        st.session_state.selected_square
    )

    if selected_piece is not None:

        color_name = (
            "백"
            if selected_piece.color == chess.WHITE
            else "흑"
        )

        piece_name = PIECE_NAMES[
            selected_piece.piece_type
        ]

        target_count = len(legal_targets)

        st.caption(
            f"선택한 말: {color_name} {piece_name}  "
            f"• 이동 가능: {target_count}칸"
        )


# ============================================================
# 기보
# ============================================================

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


# ============================================================
# 게임 종료
# ============================================================

if board.is_game_over():

    st.divider()

    if board.is_checkmate():

        winner = (
            "흑"
            if board.turn == chess.WHITE
            else "백"
        )

        st.success(
            f"🏆 게임 종료 — {winner} 승리!"
        )

    elif board.is_stalemate():

        st.info(
            "🤝 게임 종료 — 스테일메이트 무승부"
        )

    elif board.is_insufficient_material():

        st.info(
            "🤝 게임 종료 — 기물 부족으로 무승부"
        )

    elif board.is_seventyfive_moves():

        st.info(
            "🤝 게임 종료 — 75수 규칙으로 무승부"
        )

    elif board.is_fivefold_repetition():

        st.info(
            "🤝 게임 종료 — 동일 포지션 5회 반복"
        )
