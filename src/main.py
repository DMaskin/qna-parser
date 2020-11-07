import question_parser as parser
import json_writer
import time

jsonFileName = 'questions.json'

if __name__ == "__main__":
    # диапазон вопросов для парсинга:
    startId = 4
    endId = 10

    start_time = time.time()

    for questionId in range(startId, endId):
        parsedQuestion = parser.getParsedQuestion(questionId)
        if (parsedQuestion != None):
            json_writer.writeJSONtoFile(jsonFileName, parsedQuestion)

    print(f'Время выполнения: {(time.time() - start_time):.3} сек.')
