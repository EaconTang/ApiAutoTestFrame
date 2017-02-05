## 可扩展的接口自动测试框架

### 框架设计
(Github显示可能有问题，原图链接在这)http://qn.tangyingkang.com/image/blog/apitest/01.jpeg  

![](http://qn.tangyingkang.com/image/blog/apitest/01.jpeg)

### 测试用例
通过json/yaml文件等方式定义测试用例，实现代码与数据分离。一个用例文件如下：  
    
    {
      "name": "用例名称",
      "author": "用例作者",
      "createTime": "(可选)创建时间",
      "lastModifyTime": "(可选)最后修改时间",
      "lastModifiedAuthor": "(可选)最后修改人",
      "summary": "用例描述",
      "comment": "(可选)备注说明",
      "precondition": {
        "version": "系统版本",
        "function": [
          {
            "prefunc": "前置函数名称",
            "args": [
              {
                "name": "参数名",
                "type": "参数数据类型",
                "value": "参数值"
              }
            ]
          }
        ],
        "dependency": [
          "依赖接口1",
          "依赖接口2",
          "..."
        ]
      },
      "step": [
        {
          "input": {
            "http": {
              "version": "HTTP协议版本",
              "ip": "HTTP请求的IP地址",
              "port": "HTTP请求的端口",
              "path": "HTTP请求的路径",
              "url": "HTTP请求的完整URL",
              "method": "GET/POST/DELETE",
              "param": [
                {
                  "name": "参数名",
                  "type": "参数数据类型",
                  "value": "参数值"
                }
              ]
            },
            "cm": {
              "server": "webadmin",
              "cmd": "01",
              "param": [
                {
                  "name": "参数名",
                  "type": "参数数据类型",
                  "value": "参数值"
                }
              ]
            }
          },
          "output": {
            "strict": "严格匹配，不允许返回其他变量",
            "match": [
              {
                "var": "输出的变量名",
                "opt": "比较运算符（大于／等于／小于／不等于／加减N/正则满足/...）",
                "val": {
                  "type": "期望数据类型",
                  "value": "期望数据的值"
                }
              }
            ]
          }
        }
      ]
    }


### 运行示例
    import os
    from src import task


    def main():
        """"""
        _case_path = os.path.join(os.path.dirname(__file__), 'case', 'sample.json')
        testcase =task.OneCase(case_path=_case_path)
        testcase.run()

        # 输出结果:

        # 测试通过时:
        #   All steps passed for case: test

        # 测试不通过:
        #   Failed on case: test
        #   Step 1 failed for reason:
        #       Not equal!
        #       Expect: 201
        #       Got: 200
  

### 扩展接口协议
可通过继承IConnection类来实现私有协议接口的测试，IConnection类定义如下，只需要实现send和response方法：  

    from abc import ABCMeta, abstractmethod, abstractproperty


    class IConnection(object):
        """Connection interface for different connection in different protocol"""
        __metaclass__ = ABCMeta

        def __init__(self, *args, **kwargs):
            self.name = None

        @abstractmethod
        def send(self, *args, **kwargs):
            raise NotImplementedError

        @abstractproperty
        def response(self, *args, **kwargs):
            raise NotImplementedError
