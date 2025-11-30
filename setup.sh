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
  django-admin startproject config .
done

echo "Folders are ready"