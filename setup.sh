current_path=$(pwd)
date_caps=$(date +%b%d)
date=${date_caps,,}
folders=("lesson" "homework")


echo "Today's Date: ${date}"

mkdir $date

for f in "${folders[@]}"; do
  cd $current_path/$date || return
  mkdir $f
  cd $f || return
  virtualenv .venv
  source .venv/bin/activate
  pip install django
  pip freeze > requirements.txt
  django-admin startproject config .
done

echo "Folders are ready"