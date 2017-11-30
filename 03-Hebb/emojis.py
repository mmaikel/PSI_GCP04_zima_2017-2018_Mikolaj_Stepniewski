
class Emoji:
    def getEmoji(self, name):
        return {
            'sad':
                [
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, -1, 1, -1, -1, 1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, -1, 1, 1, 1, 1, -1, -1,
                    -1, 1, -1, -1, -1, -1, 1, -1,
                    -1, 1, -1, -1, -1, -1, 1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1
                ],
            'smile':
                [
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, -1, 1, -1, -1, 1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, 1, 1, 1, 1, 1, 1, -1,
                    -1, 1, -1, -1, -1, -1, 1, -1,
                    -1, -1, 1, 1, 1, 1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1
                ],
            'angry':
                [
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, -1, 1, -1, -1, 1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, -1, -1, 1, 1, -1, -1, -1,
                    -1, -1, 1, -1, -1, 1, -1, -1,
                    -1, 1, -1, -1, -1, -1, 1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1
                ],
            'xD':
                [
                    -1, -1, 1, -1, -1, 1, -1, -1,
                    -1, -1, -1, 1, 1, -1, -1, -1,
                    -1, -1, 1, -1, -1, 1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, 1, 1, 1, 1, 1, 1, -1,
                    -1, 1, -1, -1, -1, -1, 1, -1,
                    -1, -1, 1, 1, 1, 1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1
                ],
            'confused':
                [
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, -1, 1, -1, -1, 1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, 1, 1, 1, 1, 1, 1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1,
                    -1, -1, -1, -1, -1, -1, -1, -1
                ]
        }.get(name, -1)
