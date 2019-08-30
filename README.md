#### 有点词典命令行查询

通过requests对有道智云API请求得到翻译结果输出到命令行终端

推荐将youdao.py改为隐藏文件,然后在.zshrc或.bashrc中设置别名能够更方便的使用

例如:
```
alias d="python3 ~/.youdao.py"
```

使用:
```
d The words or sentences you need to translate.
```
