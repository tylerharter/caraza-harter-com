def is_prime(x):
  """For a given positive integer x, return True if x is prime, False otherwise."""
  y = 2
  while y < x:
    if x%y==0:
      return False
    y += 1
  return True