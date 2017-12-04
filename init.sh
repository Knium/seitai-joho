for i in `seq 1 7`; do
    mkdir ${i}
done
mkdir images
pip install -r pip-requirements.txt
chmod +x cli.py