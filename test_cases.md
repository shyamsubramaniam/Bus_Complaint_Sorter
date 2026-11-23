# Bus Complaint Sorter – Test Cases

## Test Case 1: Bus Delay
**Input:** Route 4 bus came 25 minutes late again today.

**Expected Output:**
- Category: delay
- Urgent: False
- Route: 4

## Test Case 2: Overcrowding
**Input:** The bus on route 7 is always overcrowded in the morning.

**Expected Output:**
- Category: crowding
- Urgent: False
- Route: 7

## Test Case 3: Driver Safety
**Input:** Driver on route 7 was talking on the phone while driving.

**Expected Output:**
- Category: driver
- Urgent: True
- Route: 7

## Test Case 4: Vehicle Problem
**Input:** The AC in route 2 bus is not working.

**Expected Output:**
- Category: vehicle
- Urgent: False
- Route: 2

## Test Case 5: Vague Complaint
**Input:** Why is this happening every day?

**Expected Output:**
- Category: other
- Urgent: False
- Route: None

## Test Result
These test cases check whether the program identifies complaint categories, detects safety risks, extracts route numbers, and handles vague complaints.