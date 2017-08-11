// a buffer for this functions
char buffer[20] = {0};

/**
 * Write the argument number to the str char* as an ASCII string
 *
 * @return the length of the string
 */
int writeNumber (int number)
{
  char *cursor = buffer;

  // if the number is zero
  if (number == 0)
    {
      buffer[0] = '0';       // write '0' in the first index
      buffer[1] = 0;         // null terminate the string
      return 1;           // return the length of the string (1)
    }

  int isNegative = 0;

  // if the number is negative
  if (number < 0)
    {
      isNegative = 1;     // we need to remember the sign
      number *= -1;       // multiply by -1 to make it +ve
      cursor++;           // leave a byte for the '-' symbol
    }

  int counter = number;

  // while the number is +ve
  while (counter > 0)
    {
      counter /= 10;      // remove the 'once' of the number
      cursor++;           // push the cursor to the right
    }

  *cursor = 0;            // null byte terminate
  cursor--;               // pull the cursor to the left

  // until i break the loop
  while (1)
    {
      *cursor = (char) ((number % 10) + '0');    // get the last digit of the number and add the '0' value
      number /= 10;                               // get rid of the last digit
      counter++;                                  // add one to the digit counter
      if (cursor == buffer) break;                // if we get to the first byte ... break
      cursor--;                                   // pull the cursor to the left
    }

  if (isNegative) *cursor = '-';         // if the number WAS negative add the -ve sign at the beginning

  return counter;
}

/**
 * Read the buffer string and return the integer value if implies
 *
 * @return the integer which is represented in ASCII on buffer string
 */
int readNumber ()
{
  char *cursor = buffer;

  if (buffer[0] == '-') cursor++;       // if the first character is -ve sign skip it

  int number = 0;

  // loop until we found a null byte (0)
  while (*cursor)
    {
      int ch = *cursor - '0';             // get the current character and subtract '0' from it
      if (ch < 0 || ch > 9) break;         // break if u found a number < 0 or > 9
      number *= 10;                       // multiply by 10
      number += ch;                       // add the number
      cursor++;                           // advance the cursor
    }

  if (buffer[0] == '-') number *= -1;     // multiply by -1 if the string start with -ve sign

  return number;                          // return the number
}
