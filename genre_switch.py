# Genre switching logic based on BPM
def determine_genre_from_bpm(bpm):
    genre_map = {(60, 90): 'bass_mode', (90, 115): 'basshouse_mode', (115, 125): 'house_mode', (125, 135): 'techno_mode'}
    for (low, high), mode in genre_map.items():
        if low <= bpm < high:
            return mode
    return None
