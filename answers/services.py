class СheckAnswersService(object):
    @staticmethod
    def normalize_answer(answer):
        answer = answer.strip()
        answer = answer.lower()
        answer = answer.replace(',', '.')
        return answer

    @staticmethod
    def check_answer(user_answer):
        answer1 = СheckAnswersService.normalize_answer(user_answer.answer)
        answer2 = СheckAnswersService.normalize_answer(user_answer.task.answer)
        return answer1 == answer2
