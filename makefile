setup:
	./adb-testing/adb devices > log.txt 2>&1

sendMessage:
	./adb-testing/adb shell am force-stop com.pinwheel.messenger
	./adb-testing/adb shell monkey -p com.pinwheel.messenger -c android.intent.category.LAUNCHER 1 > log.txt 2>&1
	sleep 5
	./adb-testing/adb shell input tap 250 400
	sleep 5
	./adb-testing/adb shell input tap 250 2250
	./adb-testing/adb shell input text "insert%syour%stext%shere"
	./adb-testing/adb shell input tap 1000 1450

