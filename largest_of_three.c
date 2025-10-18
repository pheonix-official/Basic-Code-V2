#include <stdio.h>

int main() {
    double n1, n2, n3;

    printf("Enter three different numbers: ");
    scanf("%lf %lf %lf", &n1, &n2, &n3);

    // if n1 is greater than both n2 and n3, n1 is the largest
    if (n1 >= n2 && n1 >= n3)
        printf("%.2lf is the largest number.\n", n1);

    // if n2 is greater than both n1 and n3, n2 is the largest
    else if (n2 >= n1 && n2 >= n3)
        printf("%.2lf is the largest number.\n", n2);

    // if neither n1 nor n2 is the largest, n3 must be the largest
    else
        printf("%.2lf is the largest number.\n", n3);

    return 0;
}