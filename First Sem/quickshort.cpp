#include <iostream>
#include <vector>
#include <thread>
#include <algorithm>
#include <chrono>

const int MIN_THREAD_SIZE = 100; // Minimum size of subarray to create new threads

// Function declarations
int partition(std::vector<int>& arr, int low, int high);
void quickSort(std::vector<int>& arr, int low, int high);

int partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; ++j) {
        if (arr[j] < pivot) {
            ++i;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}

void parallelQuickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pivotIndex = partition(arr, low, high);

        if (high - low > MIN_THREAD_SIZE) {
            // Capture variables explicitly by value for the threads
            std::thread leftThread([=, &arr]() { parallelQuickSort(arr, low, pivotIndex - 1); });
            std::thread rightThread([=, &arr]() { parallelQuickSort(arr, pivotIndex + 1, high); });

            leftThread.join();
            rightThread.join();
        } else {
            // For small chunks, use sequential quicksort
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
}

void quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);

        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

int main() {
    std::vector<int> arr = {622, 368, 359, 707, 201, 494, 852, 273, 35, 286, 436, 159, 282, 568, 977, 501, 362, 804, 570, 67, 442, 723, 848, 216, 659, 591, 414, 235, 460, 931};
    std::vector<int> arr2 = arr;

    std::cout << "Unsorted array: " << std::endl;
    for (const int& num : arr) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    // Measure parallel quicksort time
    auto start = std::chrono::high_resolution_clock::now();
    parallelQuickSort(arr, 0, arr.size() - 1);
    auto stop = std::chrono::high_resolution_clock::now();
    auto parallelquicksort_executiontime = stop - start;

    std::cout << "==========================================================================================" << std::endl;
    std::cout << "Sorted array using Parallel Quick Sort: " << std::endl;
    for (const int& num : arr) {
        std::cout << num << " ";
    }
    std::cout << std::endl << "Time taken by Parallel Quick Sort: " 
              << std::chrono::duration<double, std::milli>(parallelquicksort_executiontime).count() << " ms" << std::endl;

    // Measure sequential quicksort time
    start = std::chrono::high_resolution_clock::now();
    quickSort(arr2, 0, arr2.size() - 1);
    stop = std::chrono::high_resolution_clock::now();
    auto quicksort_executiontime = stop - start;

    std::cout << "==========================================================================================" << std::endl;
    std::cout << "Sorted array using Sequential Quick Sort: " << std::endl;
    for (const int& num : arr2) {
        std::cout << num << " ";
    }
    std::cout << std::endl << "Time taken by Sequential Quick Sort: " 
              << std::chrono::duration<double, std::milli>(quicksort_executiontime).count() << " ms" << std::endl;

    return 0;
}
