URL_TO_CHECK="$1"

echo "Checking $URL_TO_CHECK"

muffet \
    --exclude '8080\/\S*\.pdf' \
    --exclude 'upwork.com' \
    --exclude 'sitearchief.nl' \
    --exclude 'opengis.net' \
    --exclude 'https://www.nen.nl/nen-7513-2024-nl-329182' \
    --header 'user-agent:Curl' \
    --ignore-fragments \
    --one-page-only \
    --format=json \
    --buffer-size 8192 \
    $URL_TO_CHECK
