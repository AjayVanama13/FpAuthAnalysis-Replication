#!/bin/bash
ANDROID_JARS=~/android-sdk/platforms
FLOWDROID=~/fpauth-tools/flowdroid.jar
APK_DIR=apks
RESULTS_DIR=results/reachability

mkdir -p $RESULTS_DIR

for apk in $APK_DIR/*.apk; do
    name=$(basename "$apk" .apk)
    echo "Analyzing $name..."
    timeout 300 java -Xmx4g -jar $FLOWDROID \
        -a "$apk" \
        -p "$ANDROID_JARS" \
        -s SourcesAndSinks_fingerprint.txt \
        --callgraph SPARK \
        --output "$RESULTS_DIR/${name}_callgraph.xml" \
        2> "$RESULTS_DIR/${name}.log" \
        || echo "$name: timed out or failed"
done
