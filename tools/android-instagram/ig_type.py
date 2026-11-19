"""Unicode text entry into the dedicated social emulator. Public captions only."""
import base64, subprocess, sys
args=sys.argv[1:]
clear='--clear' in args
args=[x for x in args if x!='--clear']
assert len(args)==1, 'Usage: ig_type.py [--clear] "public text"'
adb=['adb','-s','emulator-5580','shell','am','broadcast']
if clear:subprocess.run(adb+['-a','ADB_CLEAR_TEXT'],check=True,capture_output=True)
encoded=base64.b64encode(args[0].encode()).decode()
subprocess.run(adb+['-a','ADB_INPUT_B64','--es','msg',encoded],check=True,capture_output=True)
print('Public text entered; verify field before publishing')
