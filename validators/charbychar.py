import lib
class CharByChar(lib.Validator):
    def __init__(self):
        super(CharByChar, self).__init__()
    def judge(self, filea, fileb):
        contenta = "\n".join(self.filea_read())
        contentb = "\n".join(self.fileb_read())
        if len(contenta) != len(contentb):
            lib.report("WA", "The length of the two files differ. Sizes are (" + str(len(contenta)) + " and " + str(len(contentb)) + ").")
            return
        for i in range(len(contenta)):
            if contenta[i] != contentb[i]:
                lib.report("WA", "Char %d differ. Read %s and %s." % (i, lib.escape(contenta[i]), lib.escape(contentb[i])))
                return
        lib.report("AC", "Accepted.")
        return
judger = CharByChar()
judger()