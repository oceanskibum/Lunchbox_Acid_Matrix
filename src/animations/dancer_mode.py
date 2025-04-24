# Motion-Reactive Animation Mode

def animate_from_motion(magnitude):
    if magnitude > 25000:
        print("🕺 Full body bounce!")
    elif magnitude > 15000:
        print("💃 Sway detected.")
    else:
        print("Standing still.")
