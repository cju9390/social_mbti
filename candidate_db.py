"""
후보 데이터베이스 관리 모듈 (SQLite)
- 후보 등록 / 조회 / 삭제
"""

import sqlite3
import json
from contextlib import contextmanager
from mbti_predict import predict_mbti

DB_PATH = "candidates.db"


@contextmanager
def _conn():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def init_db():
    """테이블 초기화 (없으면 생성)"""
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                mbti       TEXT    NOT NULL,
                axis_pct   TEXT    NOT NULL,
                created_at TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
            )
        """)


def add_candidate(name: str, answers: list) -> int:
    """
    후보 추가. answers: 20개 응답 (-3~3)
    반환: 삽입된 row id
    """
    result = predict_mbti(answers)
    with _conn() as con:
        cur = con.execute(
            "INSERT INTO candidates (name, mbti, axis_pct) VALUES (?,?,?)",
            (name, result['mbti'], json.dumps(result['axis_pct'])),
        )
        return cur.lastrowid


def _add_candidate_raw(name: str, mbti: str, axis_pct: dict) -> int:
    """MBTI·axis_pct 직접 지정해서 삽입 (SVM 미사용)"""
    with _conn() as con:
        cur = con.execute(
            "INSERT INTO candidates (name, mbti, axis_pct) VALUES (?,?,?)",
            (name, mbti, json.dumps(axis_pct)),
        )
        return cur.lastrowid


def add_candidate_from_result(name: str, result: dict) -> int:
    """predict_mbti() 결과 딕셔너리를 받아 저장. 이름 중복 시 덮어씀."""
    mbti     = result['mbti']
    axis_pct = json.dumps(result['axis_pct'])
    with _conn() as con:
        existing = con.execute(
            "SELECT id FROM candidates WHERE name = ?", (name,)
        ).fetchone()
        if existing:
            con.execute(
                "UPDATE candidates SET mbti=?, axis_pct=? WHERE name=?",
                (mbti, axis_pct, name),
            )
            return existing['id']
        else:
            cur = con.execute(
                "INSERT INTO candidates (name, mbti, axis_pct) VALUES (?,?,?)",
                (name, mbti, axis_pct),
            )
            return cur.lastrowid


def seed_candidates():
    """16개 MBTI 유형 각 1명씩 예시 후보 삽입"""
    # (이름, MBTI, {축: 우세측 퍼센트})
    # 각 축 쌍(E/I, N/S, T/F, J/P)의 합이 100이 되도록 설정
    seeds = [
        ("테스트1", "INTJ", {"E": 28, "I": 72, "N": 78, "S": 22, "T": 75, "F": 25, "J": 70, "P": 30}),
        ("테스트2", "INTP", {"E": 25, "I": 75, "N": 72, "S": 28, "T": 78, "F": 22, "J": 32, "P": 68}),
        ("테스트3", "ENTJ", {"E": 72, "I": 28, "N": 75, "S": 25, "T": 73, "F": 27, "J": 68, "P": 32}),
        ("테스트4", "ENTP", {"E": 70, "I": 30, "N": 73, "S": 27, "T": 72, "F": 28, "J": 30, "P": 70}),
        ("테스트5", "INFJ", {"E": 27, "I": 73, "N": 76, "S": 24, "T": 28, "F": 72, "J": 71, "P": 29}),
        ("테스트6", "INFP", {"E": 26, "I": 74, "N": 74, "S": 26, "T": 25, "F": 75, "J": 31, "P": 69}),
        ("테스트7", "ENFJ", {"E": 71, "I": 29, "N": 72, "S": 28, "T": 26, "F": 74, "J": 69, "P": 31}),
        ("테스트8", "ENFP", {"E": 73, "I": 27, "N": 76, "S": 24, "T": 27, "F": 73, "J": 29, "P": 71}),
        ("테스트9", "ISTJ", {"E": 24, "I": 76, "N": 23, "S": 77, "T": 74, "F": 26, "J": 72, "P": 28}),
        ("테스트10", "ISFJ", {"E": 26, "I": 74, "N": 25, "S": 75, "T": 27, "F": 73, "J": 70, "P": 30}),
        ("테스트11", "ESTJ", {"E": 74, "I": 26, "N": 24, "S": 76, "T": 76, "F": 24, "J": 71, "P": 29}),
        ("테스트12", "ESFJ", {"E": 72, "I": 28, "N": 26, "S": 74, "T": 25, "F": 75, "J": 68, "P": 32}),
        ("테스트13", "ISTP", {"E": 25, "I": 75, "N": 22, "S": 78, "T": 77, "F": 23, "J": 28, "P": 72}),
        ("테스트14", "ISFP", {"E": 28, "I": 72, "N": 24, "S": 76, "T": 24, "F": 76, "J": 30, "P": 70}),
        ("테스트15", "ESTP", {"E": 75, "I": 25, "N": 23, "S": 77, "T": 73, "F": 27, "J": 29, "P": 71}),
        ("테스트16", "ESFP", {"E": 76, "I": 24, "N": 25, "S": 75, "T": 26, "F": 74, "J": 31, "P": 69}),
    ]
    for name, mbti, axis_pct in seeds:
        _add_candidate_raw(name, mbti, axis_pct)
    print(f"{len(seeds)}명 예시 후보 추가 완료")


def get_all_candidates() -> list[dict]:
    """DB의 모든 후보를 predict_mbti 결과 형식으로 반환"""
    with _conn() as con:
        rows = con.execute(
            "SELECT name, mbti, axis_pct FROM candidates ORDER BY id"
        ).fetchall()

    return [
        {
            "name": row['name'],
            "result": {
                "mbti":     row['mbti'],
                "proba":    [],
                "axis_pct": json.loads(row['axis_pct']),
            },
        }
        for row in rows
    ]


def remove_candidate(name: str) -> int:
    """이름으로 후보 삭제. 반환: 삭제된 행 수"""
    with _conn() as con:
        cur = con.execute("DELETE FROM candidates WHERE name = ?", (name,))
        return cur.rowcount


def list_candidates() -> list[dict]:
    """후보 목록 (id, name, mbti, created_at) 반환"""
    with _conn() as con:
        rows = con.execute(
            "SELECT id, name, mbti, created_at FROM candidates ORDER BY id"
        ).fetchall()
    return [dict(r) for r in rows]


def clear_candidates():
    """모든 후보 삭제 + ID 시퀀스 초기화"""
    with _conn() as con:
        con.execute("DELETE FROM candidates")
        con.execute("DELETE FROM sqlite_sequence WHERE name='candidates'")



if __name__ == '__main__':
    init_db()
    clear_candidates()
    seed_candidates()
    for c in list_candidates():
        print(c)