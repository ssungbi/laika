import codecs

script = codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'r', 'utf-8').read()

first_idx = script.find('"v9902_life": {')
second_idx = script.find('"v9902_life": {', first_idx + 10)

if second_idx != -1:
    # Delete the first one
    # Find the end of the first one
    # Wait, in the first one, it's immediately followed by some other key?
    # No, it was added right at the start of allDisabilityData!
    # The next key should be the FIRST key that was originally in allDisabilityData, which is "v1804" or similar.
    # Actually, the original file had:
    # const allDisabilityData = {
    #     "v1804": [
    # So if I find `"v1804": [`, I can delete everything from first_idx to there!
    # Wait, I checked v1804 earlier and it was there. Let's find `"v1804":`
    v1804_idx = script.find('"v1804":')
    if v1804_idx != -1 and v1804_idx > first_idx and v1804_idx < second_idx:
        script = script[:first_idx] + script[v1804_idx:]
        codecs.open('c:/Users/SB/Desktop/연습용/script.js', 'w', 'utf-8').write(script)
        print("Deleted duplicate v9902_life successfully.")
    else:
        print(f"Could not safely delete. v1804_idx: {v1804_idx}, first: {first_idx}, second: {second_idx}")
else:
    print("Only one v9902_life found.")
