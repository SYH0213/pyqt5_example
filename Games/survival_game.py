

import random
import time

# --- 게임 상태 변수 ---
# 게임의 모든 데이터를 저장하는 딕셔너리입니다.
player = {
    'hp': 100,              # 플레이어의 현재 체력
    'max_hp': 100,          # 플레이어의 최대 체력
    'action_points': 5,     # 하루에 할 수 있는 행동의 수
    'day': 1,               # 현재 날짜
    'inventory': {
        'fish': 0,          # 날 생선 개수
        'cooked_fish': 0,   # 구운 생선 개수
        'pork': 0,          # 생 돼지고기 개수
        'cooked_pork': 0,   # 구운 돼지고기 개수
        'wood': 0,          # 나무 개수
        'rope': 0,          # 줄 개수
        'canned_food': 0,   # 통조림 개수
        'relic': 0,         # 유물 개수
    },
    'has_campfire': False,  # 모닥불 보유 여부
}

# --- 유틸리티 함수 ---

def print_status():
    """플레이어의 현재 상태를 출력합니다."""
    print("\n--- 상태 ---")
    print(f"날짜: {player['day']}일차")
    print(f"체력: {player['hp']}/{player['max_hp']}")
    print(f"행동력: {player['action_points']}")
    print("--- 소지품 ---")
    for item, count in player['inventory'].items():
        if count > 0:
            print(f"- {item_korean_name(item)}: {count}개")
    if player['has_campfire']:
        print("- 모닥불 보유 중")
    print("-------------")

def use_action_point():
    """행동력을 1 소모하고, 행동력이 없으면 하루를 넘깁니다."""
    player['action_points'] -= 1
    print("행동력을 1 소모했습니다.")
    if player['action_points'] <= 0:
        next_day()

def next_day():
    """다음 날로 넘어가고, 상태를 업데이트합니다."""
    player['day'] += 1
    player['hp'] -= 20
    player['action_points'] = 5
    print("\n*** 밤이 깊어 잠에 듭니다... ***")
    time.sleep(1)
    print(f"*** {player['day']}일차 아침이 밝았습니다. ***")
    print("피로가 몰려와 체력이 20 감소했습니다.")
    if player['hp'] <= 0:
        game_over()

def game_over():
    """게임 오버 메시지를 출력하고 게임을 종료합니다."""
    print("\n################################")
    print("#                              #")
    print("#          GAME OVER           #")
    print("#                              #")
    print("################################")
    print(f"당신은 {player['day']}일차에 무인도에서 생존하지 못했습니다...")
    exit()

def game_win():
    """게임 승리 메시지를 출력하고 게임을 종료합니다."""
    print("\n********************************")
    print("*                              *")
    print("*        탈출 성공!        *")
    print("*                              *")
    print("********************************")
    print(f"당신은 {player['day']}일차에 뗏목을 만들어 무인도를 탈출했습니다!")
    exit()

def item_korean_name(item_key):
    """아이템 키를 한글 이름으로 변환합니다."""
    names = {
        'fish': '날 생선',
        'cooked_fish': '구운 생선',
        'pork': '생 돼지고기',
        'cooked_pork': '구운 돼지고기',
        'wood': '나무',
        'rope': '줄',
        'canned_food': '통조림',
        'relic': '유물',
    }
    return names.get(item_key, item_key)

# --- 행동 함수 ---

def go_fishing():
    """낚시를 해서 물고기를 잡습니다."""
    print("\n낚시를 시작합니다...")
    time.sleep(1)
    player['inventory']['fish'] += 1
    print("물고기를 1마리 잡았습니다!")
    use_action_point()

def go_hunting():
    """사냥을 해서 돼지를 잡거나 다칩니다."""
    print("\n멧돼지를 사냥하러 숲으로 들어갑니다...")
    time.sleep(1)
    if random.random() < 0.6:  # 60% 확률로 성공
        print("사냥에 성공하여 돼지고기를 얻었습니다!")
        player['inventory']['pork'] += 1
    else:
        print("멧돼지의 공격을 받아 다쳤습니다! HP가 20 감소합니다.")
        player['hp'] -= 20
        if player['hp'] <= 0:
            game_over()
    use_action_point()

def gather_resources():
    """자원 채집 메뉴를 보여주고 선택에 따라 행동합니다."""
    while True:
        print("\n--- 자원 채집 ---")
        print("1. 나무 캐기")
        print("2. 주변 탐색하기 (랜덤 아이템)")
        print("3. 돌아가기")
        choice = input("무엇을 하시겠습니까? >> ")

        if choice == '1':
            print("\n나무를 캡니다...")
            time.sleep(1)
            player['inventory']['wood'] += 1
            print("나무를 1개 얻었습니다.")
            use_action_point()
            break
        elif choice == '2':
            print("\n주변을 탐색합니다...")
            time.sleep(1)
            rand_val = random.random()
            if rand_val < 0.05: # 5% 확률로 유물
                print("반짝이는 유물을 발견했습니다! 최대 체력이 100 증가합니다!")
                player['inventory']['relic'] += 1
                player['max_hp'] += 100
            elif rand_val < 0.3: # 25% 확률로 줄 (5% + 25%)
                print("튼튼한 줄을 발견했습니다!")
                player['inventory']['rope'] += 1
            else: # 70% 확률로 통조림
                print("누군가 먹다 남긴 통조림을 발견했습니다.")
                player['inventory']['canned_food'] += 1
            use_action_point()
            break
        elif choice == '3':
            break
        else:
            print("잘못된 입력입니다.")

def craft_and_eat():
    """제작 및 먹기 메뉴를 보여줍니다."""
    while True:
        print("\n--- 제작 및 먹기 ---")
        print("1. 모닥불 피우기 (나무 3개 필요)")
        print("2. 음식 굽기/먹기")
        print("3. 뗏목 만들기 (나무 20개, 줄 5개 필요)")
        print("4. 돌아가기")
        choice = input("무엇을 하시겠습니까? >> ")

        if choice == '1':
            if player['has_campfire']:
                print("이미 모닥불이 있습니다.")
            elif player['inventory']['wood'] >= 3:
                player['inventory']['wood'] -= 3
                player['has_campfire'] = True
                print("나무 3개를 사용해 모닥불을 만들었습니다. 이제 음식을 구울 수 있습니다.")
            else:
                print("나무가 부족합니다.")
        elif choice == '2':
            eat_food()
        elif choice == '3':
            build_raft()
        elif choice == '4':
            break
        else:
            print("잘못된 입력입니다.")

def eat_food():
    """음식 먹기/굽기 메뉴"""
    while True:
        print("\n--- 음식 ---")
        print(f"1. 생선 굽기 (HP+10, 모닥불 필요) - 보유: {player['inventory']['fish']}개")
        print(f"2. 돼지고기 굽기 (HP+50, 모닥불 필요) - 보유: {player['inventory']['pork']}개")
        print(f"3. 통조림 먹기 (HP+30) - 보유: {player['inventory']['canned_food']}개")
        print("4. 돌아가기")
        choice = input("어떤 음식을 드시겠습니까? >> ")

        if choice == '1':
            if player['has_campfire']:
                if player['inventory']['fish'] > 0:
                    player['inventory']['fish'] -= 1
                    player['hp'] = min(player['max_hp'], player['hp'] + 10)
                    print("생선을 구워 먹었습니다. HP가 10 회복됩니다.")
                    use_action_point()
                else:
                    print("구울 생선이 없습니다.")
            else:
                print("모닥불이 없어서 구울 수 없습니다.")
        elif choice == '2':
            if player['has_campfire']:
                if player['inventory']['pork'] > 0:
                    player['inventory']['pork'] -= 1
                    player['hp'] = min(player['max_hp'], player['hp'] + 50)
                    print("돼지고기를 구워 먹었습니다. HP가 50 회복됩니다.")
                    use_action_point()
                else:
                    print("구울 돼지고기가 없습니다.")
            else:
                print("모닥불이 없어서 구울 수 없습니다.")
        elif choice == '3':
            if player['inventory']['canned_food'] > 0:
                player['inventory']['canned_food'] -= 1
                player['hp'] = min(player['max_hp'], player['hp'] + 30)
                print("통조림을 먹었습니다. HP가 30 회복됩니다.")
                use_action_point()
            else:
                print("먹을 통조림이 없습니다.")
        elif choice == '4':
            break
        else:
            print("잘못된 입력입니다.")

def build_raft():
    """뗏목을 만들어 게임에서 승리합니다."""
    if player['inventory']['wood'] >= 20 and player['inventory']['rope'] >= 5:
        print("\n충분한 재료가 있습니다! 뗏목을 만들어 무인도를 탈출합니다!")
        time.sleep(2)
        game_win()
    else:
        print("\n뗏목을 만들 재료가 부족합니다.")
        print(f"- 필요 재료: 나무 20개 (보유: {player['inventory']['wood']}), 줄 5개 (보유: {player['inventory']['rope']})")

# --- 메인 게임 루프 ---

def main():
    """메인 게임 루프를 실행합니다."""
    print("눈을 떠보니 무인도에 표류해있었습니다...")
    print("살아남고, 뗏목을 만들어 탈출해야 합니다!")

    while True:
        print_status()
        print("\n--- 무엇을 할까? ---")
        print("1. 낚시하기")
        print("2. 사냥하기")
        print("3. 자원 채집하기")
        print("4. 제작 및 먹기")
        print("5. 그냥 잠자기 (하루 넘기기)")

        choice = input("선택 >> ")

        if choice == '1':
            go_fishing()
        elif choice == '2':
            go_hunting()
        elif choice == '3':
            gather_resources()
        elif choice == '4':
            craft_and_eat()
        elif choice == '5':
            next_day()
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")

        if player['hp'] <= 0:
            game_over()

if __name__ == "__main__":
    main()

