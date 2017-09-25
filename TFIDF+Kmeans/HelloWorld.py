import test
import  answer
import  time
# 测试文件夹/Users/wuyuhang/PycharmProjects/Test2/textFiles

start=time.clock()
stop_word_file="/Users/wuyuhang/PycharmProjects/Test2/stop_word_file.txt";
stop_words=test.stop_words(stop_word_file);

file_path="/Users/wuyuhang/PycharmProjects/Test2/files"
names,tfidf=test.get_all_vector(file_path,stop_words)



clf_labels=test.K_Means(tfidf)
answer.Merge_show(names,clf_labels)

end=time.clock()

print("===========================")
print("Running time : %s Seconds " %(end-start))
