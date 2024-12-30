import json
import CatmullRom as cmr

def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def linear(start, end, i):
    return ((end - start) * i) + start

print("filename:")
filename = input()
print("Max number of steps:")
max_steps = int(input())

key_steps = []

print("The input loop will end if any non-numerical value is input or after " + str(int(max_steps/10)) + " key steps.")
print("x and y are in inches, theta is in degrees, lift/arm are in motor ticks.")
i: int = 0
while i < max_steps/10:
    step = {}
    print("\nKey step " + ":\nx:")
    str = input()
    if is_float(str):
        step['x'] = float(str)
    else:
        break
    print("y:")
    str = input()
    if is_float(str):
        step['y'] = float(str)
    else:
        break
    print("theta:")
    str = input()
    if is_float(str):
        step['theta'] = float(str)
    else:
        break
    step['pos_tolerance'] = 0
    step['angle_tolerance'] = 0
    print("arm:")
    str = input()
    if is_float(str):
        step['arm_target'] = float(str)
    else:
        break
    step['arm_tolerance'] = 0
    print("lift:")
    str = input()
    if is_float(str):
        step['lift_target'] = float(str)
    else:
        break
    step['lift_tolerance'] = 0
    step['input'] = 0
    step['output'] = 0
    step['millis'] = 0
    key_steps.append(step)
    i += 1

for i in range(len(key_steps)):
    tolerance = ((len(key_steps)-1-(0.9999*i))/(1.001*(len(key_steps)-1))) ** 0.5
    key_steps[i]['pos_tolerance'] = tolerance
    key_steps[i]['angle_tolerance'] = tolerance
    key_steps[i]['arm_tolerance'] = tolerance
    key_steps[i]['lift_tolerance'] = tolerance

key_steps.append(key_steps[-1])

steps = []
cmr.plotKeypoint(key_steps[1].get('x'), key_steps[1].get('y'), int(max_steps/len(key_steps)))
for i in range(len(key_steps)):
    points = cmr.plotKeypoint(key_steps[i].get('x'), key_steps[i].get('y'), int(max_steps / len(key_steps)))
    if i >= 2:
        for point, j in zip(points, range(len(points))):
            step = {}
            step['x'] = point.x
            step['y'] = point.y
            step['theta'] = linear(key_steps[i-2].get('theta'), key_steps[i-1].get('theta'), j/len(points))
            step['pos_tolerance'] = linear(key_steps[i-2].get('pos_tolerance'), key_steps[i-1].get('pos_tolerance'), j/len(points))
            step['angle_tolerance'] = linear(key_steps[i-2].get('angle_tolerance'), key_steps[i-1].get('angle_tolerance'), j/len(points))
            step['arm_target'] = linear(key_steps[i-2].get('arm_target'), key_steps[i-1].get('arm_target'), j/len(points))
            step['arm_tolerance'] = linear(key_steps[i-2].get('arm_tolerance'), key_steps[i-1].get('arm_tolerance'), j/len(points))
            step['lift_target'] = linear(key_steps[i-2].get('lift_target'), key_steps[i-1].get('lift_target'), j/len(points))
            step['lift_tolerance'] = linear(key_steps[i-2].get('lift_tolerance'), key_steps[i-1].get('lift_tolerance'), j/len(points))
            step['input'] = 0
            step['output'] = 0
            step['millis'] = 0
            steps.append(step)

write_json(filename, steps)