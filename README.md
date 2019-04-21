# FollowupBot
A bot to automate followup checkups after visits, surgeries, discharges, and other key change events

### Train NLU
cd FollowupBot
```
docker run \
    -v "$PWD/nlu_data/:/app/data" \
    -v "$PWD/config/:/app/config" \
    -v "$PWD/nlu_models/:/app/models" \
    rasa/rasa_nlu:0.13.7-full \
    run \
        python -m rasa_nlu.train \
            --config /app/config/nlu_config.yml \
            --data /app/data/nlu.md \
            --path /app/models \
            --project nlu \
            --verbose
```

### Train Core
cd FollowupBot
```
docker run \
      -v $(pwd)/config:/app/config \
      -v "$(pwd)/core_data":/app/data \
      -v $(pwd)/dialogue_models:/app/models \
      rasa/rasa_core:0.12.1 \
      train \
        --domain /app/data/domain.yml \
        --stories /app/data/stories.md \
        --out models/core \
        -c /app/config/policies.yml
```

### Convert Training Data File Format
From .md to .json and visa versa
```
docker run \
    -v "$PWD/nlu_data/:/app/data" \
    -v "$PWD/config/:/app/config" \
    -v "$PWD/nlu_models/:/app/models" \
    rasa/rasa_nlu:0.13.7-full \
    run \
        python -m rasa_nlu.convert \
            --data_file /app/data/ABC.md \
            --out_file /app/data/ABC.json \
            --format json
```

### Let's go!

    git clone https://github.com/MountSinaiHealthSystem/FollowupBot.git
    cd FollowupBot
    docker-compose up
  
