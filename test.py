
def callback():
    print("Callback called")

def notifier(target=None):
    if target!= None:
        print("Notifier called with target")
        target()

def main():
    print("main")
    notifier(callback)
    print("main done")  

if __name__ == "__main__":
    import sys
    sys.exit(main())