CXX = g++-15
# 增加必要的编译选项：-O3 优化（HPC必选）, -Wall 警告, -std=c++11
CXXFLAGS = -I../common -O3 -std=c++11 -Wall -fPIC

# 目标程序
TARGET = myexp
# 所有的对象文件
OBJS = logger.o CS149intrin.o main.o

all: $(TARGET)

# 链接阶段：将所有 .o 文件链接成可执行文件
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $(TARGET)

# 编译阶段：将 .cpp 编译为 .o
logger.o: logger.cpp logger.h CS149intrin.h
	$(CXX) $(CXXFLAGS) -c logger.cpp

CS149intrin.o: CS149intrin.cpp CS149intrin.h logger.h
	$(CXX) $(CXXFLAGS) -c CS149intrin.cpp

main.o: main.cpp CS149intrin.h logger.h
	$(CXX) $(CXXFLAGS) -c main.cpp

clean:
	rm -rf *.o $(TARGET) *~ objs/
