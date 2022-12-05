DAY_TEMPLATE='def first_puzzle_solution():
    return "TBD"


def second_puzzle_solution():
    return "TBD"
'

for day_number in $(seq 24); do
  mkdir -p day"$day_number"
  touch day"$day_number"/__init__.py

  if [[ $(cat day"$day_number"/solution.py) == '' ]]; then
    echo "$DAY_TEMPLATE" > day"$day_number"/solution.py
  fi
done
