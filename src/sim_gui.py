import sys



class SimulateGui:


    def get_year_input() -> None:
        year = input("What year of F1 do you want to look up: ",)
        return year, f"year={year}"

    def get_meeting_key(Setparam) -> str:
        while True:
            try:
                key = int(input("Enter key: "))
                if key in Setparam.list_meeting_key:
                    Setparam.meeting_key = key
                    return f"meeting_key={key}"
                elif key == 0:
                    sys.exit()
            except:
                continue

    def get_session_key(Setparam) -> str:
        while True:
            try:
                key = int(input("Enter key: "))
                if key in Setparam.list_session_key:
                    Setparam.session_key = key
                    return f"session_key={key}"
                elif key == 0:
                    sys.exit()
            except:
                continue

    def choose_analysis() -> int:
        while True:
            try:
                key = int(input("Enter analysis number: "))
                
            except Exception:
                continue
            if key == 1:
                    break
            if key == 2:
                    break
            if key == 0:
                    break
        return key



    def show_tracks(tracks: list) -> None:
        for i in tracks:
            print(f"key: {i[1]} --------> Grand prix: {i[0]}")

    def show_sessions(sessions: list[str]) -> None:
        for i in sessions:
            print(f"key: {i[1]} --------> Sessions: {i[0]}")

    def show_drivers(drivers: list[str]) -> None:
        for i in drivers:
            print(f"driver number: {i['name']}   {i['number']}---------------------{i['team_name']}")
    def show_analysis_option() -> None:
        text = """ Race analysis
                        1. Session Stints 
                        2. Laps data"""
        print(text)

    