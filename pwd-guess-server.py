

import socket
import sys
import threading
import select
import time

class GameThread(threading.Thread):
    def __init__(self, sock):
        self.gamestartevent_ = threading.Event()
        self.gamereportevent_ = threading.Event()

        self.sock_ = sock 
        threading.Thread.__init__(self)
    def run(self):
        data = self.sock_.recv(1024)
        self.player_ = data.decode('UTF-8')
        print(self.player_, "joined the game")
        player_scores[self.player_] = 0
        self.gamestartevent_.wait()

        success_msg = "success".encode('UTF-8')
        repeat_msg = "repeat".encode('UTF-8')
        failure_msg = "failure".encode('UTF-8')
        gameover_msg = "end".encode('UTF-8')
        gamestart_msg = "start".encode('UTF-8')
        self.sock_.send(gamestart_msg)
        while self.gamestartevent_.isSet():
            ready_read, ready_write, err = select.select([self.sock_], [], [], .1)
            if len(ready_read) > 0:
                recvd = self.sock_.recv(1024)
                if not recvd:
                    break
                guess = recvd.decode('UTF-8')
                if guess in credentials:
                    if self.player_ not in credentials[guess]:
                        credentials[guess] += [self.player_]
                        print(self.player_, "got", guess)
                        self.sock_.send(success_msg)
                    else:
                        self.sock_.send(repeat_msg)
                else:
                    self.sock_.send(failure_msg)
        self.sock_.send(gameover_msg)
        self.gamereportevent_.wait()
        time.sleep(1)


    def startGame(self):
        self.gamestartevent_.set()

    def endGame(self):
        self.gamestartevent_.clear()

    def reportScore(self, score_report):
        recvd = self.sock_.recv(1024)
        print(self.player_, "finished")
        self.sock_.send(score_report.encode('UTF-8'))
        self.gamereportevent_.set()

    def join(self):
        self.sock_.close()
        threading.Thread.join(self)
        

def main():
    if len(sys.argv) < 2:
        PORT = 3001
    else:
        PORT = int(sys.argv[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((socket.gethostname(), PORT))
    except socket.error as msg:
        print('Bind failed. Error Code:', str(msg[0]),'Message', msg[1])
        sys.exit()

    print("Bound to socket on port", str(PORT))

    s.listen(15)
    print("Listening on port", str(PORT))

    threads = []
    while True:
        conn, addr = s.accept()
        t = GameThread(conn)
        threads.append(t)
        t.start()
        time.sleep(.5)
        master_input = input("Is that everyone? (y/n) ")
        if master_input == "y":
            break
    
    for thread in threads:
        thread.startGame()
    
    # game running
    print("Running...")
    time_limit = 60
    for i in range(time_limit):
        print("Time remaining:", time_limit-i)
        time.sleep(1)

    for thread in threads:
        thread.endGame()
    
    # Generage score report
    for player in player_scores:
        for answer in credentials:
            if player in credentials[answer]:
                player_scores[player] += 1
    current_max = 0
    winners = []
    for player in player_scores:
        if player_scores[player] > current_max:
            winners = [player]
            current_max = player_scores[player]
        elif player_scores[player] == current_max:
            winners += [player]
    score_report = "SCORE REPORT\n"
    for player in player_scores:
        score_report += player + ": " + str(player_scores[player]) + "\n"
    score_report += "WINNER: "
    if(len(winners) == 1):
        score_report += winners[0] + "\n"
    else:
        score_report += "It's a tie!\n"
        score_report += "Between: "
        for winner in winners:
            score_report += winner + " "

    print(score_report)
    for thread in threads:
        thread.reportScore(score_report)
    time.sleep(1)
    for thread in threads:
        thread.join()

    
    
        
        

player_scores = {}
credentials = {}
credentials["root:xc3511"] = []
credentials["root:vizxv"] = []
credentials["root:admin"] = []
credentials["admin:admin"] = []
credentials["root:888888"] = []
credentials["root:xmhdipc"] = []
credentials["root:default"] = []
credentials["root:juantech"] = []
credentials["root:123456"] = []
credentials["root:54321"] = []
credentials["support:support"] = []
credentials["root:"] = []
credentials["admin:password"] = []
credentials["root:root"] = []
credentials["root:12345"] = []
credentials["user:user"] = []
credentials["admin:"] = []
credentials["root:pass"] = []
credentials["admin:admin1234"] = []
credentials["root:1111"] = []
credentials["admin:smcadmin"] = []
credentials["admin:1111"] = []
credentials["root:666666"] = []
credentials["root:password"] = []
credentials["root:1234"] = []
credentials["root:klv123"] = []
credentials["Administrator:admin"] = []
credentials["service:service"] = []
credentials["supervisor:supervisor"] = []
credentials["guest:guest"] = []
credentials["guest:12345"] = []
credentials["admin1:password"] = []
credentials["administrator:1234"] = []
credentials["666666:666666"] = []
credentials["888888:888888"] = []
credentials["ubnt:ubnt"] = []
credentials["root:klv1234"] = []
credentials["root:Zte521"] = []
credentials["root:hi3518"] = []
credentials["root:jvbzd"] = []
credentials["root:anko"] = []
credentials["root:zlxx."] = []
credentials["root:7ujMko0vizxv"] = []
credentials["root:7ujMko0admin"] = []
credentials["root:system"] = []
credentials["root:ikwb"] = []
credentials["root:dreambox"] = []
credentials["root:user"] = []
credentials["root:realtek"] = []
credentials["root:00000000"] = []
credentials["admin:1111111"] = []
credentials["admin:1234"] = []
credentials["admin:12345"] = []
credentials["admin:54321"] = []
credentials["admin:123456"] = []
credentials["admin:7ujMko0admin"] = []
credentials["admin:1234"] = []
credentials["admin:pass"] = []
credentials["admin:meinsm"] = []
credentials["tech:tech"] = []
credentials["mother:fucker"] = []

if __name__ == "__main__":
    main()
