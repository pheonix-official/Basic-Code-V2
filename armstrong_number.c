#include <stdio.h>
#include <math.h>

int main() {
    int num, originalNum, remainder, n = 0;
    double result = 0.0;

    printf("Enter an integer: ");
    scanf("%d", &num);

    originalNum = num;

    // store the number of digits of num in n
    for (originalNum = num; originalNum != 0; ++n) {
        originalNum /= 10;
    }

    originalNum = num;

    // check if num is an Armstrong number
    for (; originalNum != 0; originalNum /= 10) {
        remainder = originalNum % 10;
        result += pow(remainder, n);
    }

    if ((int)result == num)
        printf("%d is an Armstrong number.\n", num);
    else
        printf("%d is not an Armstrong number.\n", num);

    return 0;
}