def binary_search(arr, query):
    '''Binary search'''
    low = 0
    high = len(arr) - 1
    iterations = 0

    while low <= high:
        mid = (low + high) // 2
        iterations += 1

        if arr[mid] == query:
            return iterations, arr[mid]
        elif arr[mid] < query:
            low = mid + 1
        else:
            high = mid - 1

    if high < 0:
        return (iterations, arr[0])  # Якщо значення менше ніж найменший елемент
    elif low >= len(arr):
        return (iterations, None)  # Якщо значення більше ніж найбільший елемент
    else:
        return (iterations, arr[low])  # Верхня межа

# Приклад використання:
arr = [0.1, 1.3, 4.7, 2.9, 6.1, 0.51, 0.6]
arr.sort()
print(arr)
print(binary_search(arr, 0.6))
