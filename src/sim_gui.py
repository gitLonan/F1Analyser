import sys



class SimulateGui:


    def get_year_input(setparam) -> None:
        year = input("What year of F1 do you want to look up: ",)
        _ = year.split()
        if _[1] == "new":
            print("Call this api again")
            setparam.call_again = True
        int_year = _[0]
        return int_year, f"year={int_year}"

    def get_meeting_key(Setparam) -> str:
        while True:
            try:
                key = int(input("Enter key: "))
                if key in Setparam.list_meeting_key:
                    Setparam.meeting_key = key
                    Setparam.meeting_key_attr = f"meeting_key={key}"
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
                    Setparam.session_key_attr = f"session_key={key}"
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
            return key

    def choose_drivers_for_car_data(setparam: object) -> list[int]:
        selected_drivers = []
        print("Write '123' to have all the drivers or '0' to end it")
        while True:
            
            try:
                key = int(input("Select drivers:"))
                if key not in selected_drivers and key != 0:
                    selected_drivers.append(key-1)
            except Exception:
                continue
            if key == 0:
                return selected_drivers
            elif key == 123:
                return [i for i in range(0, len(setparam.drivers))]

    def select_lap_for_car_data_analysis(lap_numbers):
        lap = 0
        while lap < 1 or lap > lap_numbers:
            try:
                lap = int(input("Select lap for analysis: "))
            except Exception:
                continue
            if lap == 0:
                sys.exit()
            
        return lap


    def show_tracks(tracks: list) -> None:
        for i in tracks:
            print(f"key: {i[1]} --------> Grand prix: {i[0]}")

    def show_sessions(sessions: list[str]) -> None:
        for i in sessions:
            print(f"key: {i[1]} --------> Sessions: {i[0]}")

    def show_drivers(drivers: list[str]) -> None:
        for i in range(0, len(drivers)):
            print(f"{i+1}. -driver number: {drivers[i]['name']}   {drivers[i]['number']}---------------------{drivers[i]['team_name']}")

    def show_analysis_option() -> None:
        text = """ Race analysis
                        1. Stints duration for all drivers 
                        2. Fastest sectors and fastest lap time
                        3. Average sectors and lap time for stints
                        4. Car data """
        print(text)

    