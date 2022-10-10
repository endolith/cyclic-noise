This is a mess.  TODO: Turn it into a function.  
It generates cyclic/repeating/perfect loop noise by low-pass filtering
white noise in a cyclic way.  Useful for "random" but looping animations, etc.:

This one loops in both space and time, for instance:

![ezgif-5-bea77d8739](https://user-images.githubusercontent.com/58611/194798892-6cabdae9-bcae-4fac-a5cf-6f8ba16ed633.gif)![ezgif-5-bea77d8739](https://user-images.githubusercontent.com/58611/194798892-6cabdae9-bcae-4fac-a5cf-6f8ba16ed633.gif)

Simplex noise typically has a more trapezoidal value distribution:

https://github.com/lmas/opensimplex/issues/18#issuecomment-796367121

which could be emulated by stretching the sample values.