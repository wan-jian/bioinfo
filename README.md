# bioinfo
临床数据分析
## 使用说明
命令的使用如下：
```
$ python3 bi.py [-h|--help] [项目文件]
```
其中“项目文件”可以省略，如省略，则使用当前工作目录下的“default.json”文件。
项目文件定义一个数据处理过程，项目文件采用JSON格式，示例如下：
```
{
  "process_name" : "process1_1",
  "comment" : "Divide clinical information into metastasis group and non-metastasis group",
  "data_dir" : "/Users/wj/data",
  "source_file" : "临床信息.xlsx",
  "output_file" : "f.xls"
}
```
其中：
* process_name：分析处理的名称
* comment：处理的描述
* data_dir：数据文件的存放目录
* source_file：待处理的文件名
* output_file：处理分析后的结果的文件名
