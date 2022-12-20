import time
from ppadb.client import Client as AdbClient
from datetime import datetime, timedelta
from tools.imageInterperate import readBenchmarkScores
from pathlib import Path
import PySimpleGUI
import os
import json


class phone():

    def __init__(self, GUI=False):
        self.usingGUI = GUI
        self.logLocation = Path("./logs/log.txt")
        self.log = open(self.logLocation, "w")
        self.client = AdbClient(host="127.0.0.1", port=5037)

        self.devices = self.client.devices()

        if len(self.devices) == 0:
            self.log.write(f'{datetime.now().strftime("%H:%M:%S")} --- No devices\n')
        else:
            self.device = self.devices[0]
            self.log.write(f'{datetime.now().strftime("%H:%M:%S")} --- Connected to {self.device}\n')

        self.screen_size = self.device.shell("wm size").split(" ")[2]
        self.screen_height = max([int(x) for x in self.screen_size.split("x")])
        self.screen_width = min([int(x) for x in self.screen_size.split("x")])

    def shell(self, command: str) -> None:
        self.device.shell(command)

    def screenshot(self):
        screenshot = self.device.screencap()
        with open('./ScreenCaptures/result.png', 'wb') as f:
            f.write(screenshot)
        self.__logAction("Screenshot Sucess")
        return "./ScreenCaptures/result.png"

    def testAntutu(self) -> list:

        if not self.isInstalled("com.antutu.benchmark.full.lite"):
            inst = [self.install("AnTuTu 3DBench Lite.apk"), self.install("antutu-benchmark-v934.apk")]
            if False in inst:
                self.__logAction("Antutu APK Does Not Exist")
                return []
            self.open("com.antutu.benchmark.full.lite")
            time.sleep(5)
            self.device.input_tap(int(self.screen_width / 2), int(self.screen_height * 0.2))
            time.sleep(2)
            self.device.input_tap(int(self.screen_width / 2), int(self.screen_height * 0.7208))
        else:
            self.open("com.antutu.benchmark.full.lite")

        time.sleep(5)        
        self.device.input_tap(int(self.screen_width / 2), int(self.screen_height * 0.32))
        self.__logAction("Benchmark Started")
        while len(self.device.shell(f"logcat -t \'{self.fiveSecondsAgo()}\'| grep com.antutu.ABenchMark/com.example.benchmark.ui.test.activity.ActivityTestResultDetails")) < 1:
            time.sleep(5)
        self.__logAction("Antutu Test Sucess")

        time.sleep(5)
        scores = readBenchmarkScores(self.screenshot(), self.screen_width, self.screen_height)
        self.device.input_tap(int(self.screen_width * 0.0792), int(self.screen_height * 0.066))

        return scores
        
    def repeatTestAntutu(self, count: int) -> dict:

        now = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
        results = { now : {"CPU": [], "GPU": [], "Memory": [], "UX": [], "Total": [], "AVG": 0}}

        self.__logAction(f"Getting test scores from {count} tests")
        for i in range(count):
            self.__logAction(f"Test {i + 1}")
            r = list(map(int, self.testAntutu()))
            if r == []:
                return "APK Not Found"
            else:
                self.__logAction(f"Test {i + 1} sucess")
                for key in list(results[now].keys())[0:4]:
                    results[now][key].append(r.pop())
                results[now]["Total"].append(sum(r))
        results[now]["AVG"] = sum(results[now]["Total"]) // count

        self.__logAction("Resturning Results")
        self.__logAction(str(results))

        with open('./TestResult/results.json', 'w') as f:
            json.dump(results, f)
            f.close()

        return results

    def fiveSecondsAgo(self) -> str:
        return (datetime.now() - timedelta(seconds=5)).strftime('%m-%d %H:%M:%S.000')
    
    def isInstalled(self, package: str) -> bool:
        packages = self.device.shell("pm list packages").split("\n")
        return "package:" + package in packages

    def __logAction(self, action: str) -> None:
        self.log.write(f'{datetime.now().strftime("%H:%M:%S")} --- ' + action + "\n")
        print(f'{datetime.now().strftime("%H:%M:%S")} --- ' + action)

    def install(self, fileName: str) -> bool:
        path = "./apks/" + fileName
        if os.path.exists(path):
            self.device.install(path)
            self.__logAction("Install Antutu")
            return True
        else:
            self.__logAction("Apk Not Found")
            return False
    
    def open(self, package: str) -> None:
        self.device.shell(f"monkey -p {package} 1")