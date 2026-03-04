#!/usr/bin/python3

class Visualizer:
    @staticmethod
    def translate(map: str, w: int, h: int) -> list[list[str]]:
        lst: list[list[str]] = [[" " for x in range(w * 3 + 2)]
                                for y in range(h * 2 + 1)]
        i: int = 0
        j: int = 0

        for char in map:
            if char == "\n":
                j = 0
                i += 2
                continue
            n: int = int(char, base=16)

            lst[i][j] = "█"
            lst[i][j + 3] = "█"
            lst[i + 2][j] = "█"
            lst[i + 2][j + 3] = "█"
            if n & 0x1:
                lst[i][j + 1] = "█"
                lst[i][j + 2] = "█"
            if n & 0x2:
                lst[i + 1][j + 3] = "█"
            if n & 0x4:
                lst[i + 2][j + 1] = "█"
                lst[i + 2][j + 2] = "█"
            if n & 0x8:
                lst[i + 1][j] = "█"
            j += 3
        return lst

    def from_translated_map(trans_map: list[list[str]]) -> None:
        for row in trans_map:
            for char in row:
                print(char, end="")
            print("")


if __name__ == "__main__":
    pass
#    Visualizer.from_translated_map(Visualizer.translate("9515391539551795151151153\nEBABAE812853C1412BA812812\n96A8416A84545412AC4282C2A\nC3A83816A9395384453A82D02\n96842A852AC07AAD13A8283C2\nC1296C43AAB83AA92AA8686BA\n92E853968428444682AC12902\nAC3814452FA83FFF82C52C42A\n85684117AFC6857FAC1383D06\nC53AD043AFFFAFFF856AA8143\n91441294297FAFD501142C6BA\nAA912AC3843FAFFF82856D52A\n842A8692A92B8517C4451552A\n816AC384468285293917A9542\nC416928513C443A828456C3BA\n91416AA92C393A82801553AAA\nA81292AA814682C6A8693C6AA\nA8442C6C2C1168552C16A9542\n86956951692C1455416928552\nC545545456C54555545444556", 25, 20))
