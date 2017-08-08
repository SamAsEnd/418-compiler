char str[20] = {0};

int writeNumber(int number) {
    char *t = str;

    if(number == 0) {
        str[0] = '0';
        str[1] = 0;
        return 1;
    }

    int neg = 0;

    if(number < 0) {
        neg = 1;
        number *= -1;
        t++;
    }

    int tmp = number;

    while (tmp > 0) {
        tmp /= 10;
        t++;
    }

    *t = 0;
    t--;

    while (1) {
        *t = number % 10 + '0';
        number /= 10;
        tmp++;
        if (t == str) break;
        t--;
    }

    if(neg) *t = '-';

    return tmp;
}

int readNumber() {
    char *t = str;
    if (str[0] == '-') t++;

    int number = 0;

    while (*t) {
        int ch = *t - '0';
        if(ch < 0 || ch > 9) break;
        number *= 10;
        number += ch;
        t++;
    }

    if (str[0] == '-') number *= -1;

    return number;
}
