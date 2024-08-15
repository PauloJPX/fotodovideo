#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Uso: $0 <arquivo_de_video> <intervalo_em_segundos> <diretorio_de_saida>"
    exit 1
fi

VIDEO_FILE=$1
INTERVAL=$2
OUTPUT_DIR=$3

if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
fi

ffmpeg -i "$VIDEO_FILE" -vf "fps=1/$INTERVAL" "$OUTPUT_DIR/frame_%04d.jpg"
