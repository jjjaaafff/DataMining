# Expectation-Maximation Algorithm

 以点集聚类为例进行说明
 * 变量说明 

    * Y为观测变量的数据，即每个点的坐标
    * Z为隐含变量的数据，即每个点所属的cluster
    * (Y,Z)联合起来就是完全数据
    * $\theta$ 为需要估计的模型参数。对于高斯模型,$\theta\sim(\mu,\sigma)$；对于伯努利分布，$\theta\sim p$
 * 优化目标

    我们想要通过极大似然估计(MLE)，用观测变量数据去确定模型参数，即
    $$\max \limits_{\theta}logP(Y|\theta) = \max \limits_{\theta}log\sum_{Z}P(Y,Z|\theta)$$
    由于Z是未知的隐变量，我们不能直接得到$P(Y,Z|\theta)$。但如果给定Y和$\theta$，我们是可以求得Z对应的条件分布$P(Z|Y,\theta)$。  
    所以我们先根据现有模型参数猜测Z的分布，再去改善模型参数。优化目标变为
    $$\max \limits_{\theta^{(t)}}E_{Z|Y,\theta^{(t-1)}}logP(Y,Z|\theta^{(t)})$$
    通过这种方式，我们绕开了Z未知的问题，优化目标现在只包含$\theta$一个未知量，而$\theta$则是通过不断迭代逼近最优值。
 * 算法流程
    
    在知道我们的优化目标后，对应的EM算法流程就很清晰了
    1. 初始化, 给出初始的模型参数$\theta^{(0)}$
    2. E-step, 计算期望值
        $$E_{Z|Y,\theta^{(t-1)}}logP(Y,Z|\theta) = \sum_{Z}P(Z|Y,\theta^{(t-1)})logP(Y,Z|\theta)$$
    3. M-step, 求使上述期望最大的$\theta$参数值
        $$\theta^{(t)} = \argmax \limits_{\theta}E_{Z|Y,\theta^{(t-1)}}logP(Y,Z|\theta)$$
    4. 重复E-step与M-step直至收敛，得到最后的$\theta$参数值，通过此模型参数去分类
 * 算法结论

    EM算法保证能够收敛，但不一定收敛到全局最优，对初始值较敏感  
    在聚类中，将内存的消耗由O(data)降至O(cluster)
 * 算法原理

    记初始对数似然函数为$L(\theta|Y) =log\sum_{Z}P(Y,Z|\theta)$  
    为什么可以将初始优化问题转化为Z的期望?  
    $$L(\theta|Y) =log\sum_{Z}P(Y,Z|\theta) = log\sum_{Z}P(Z|Y,\theta^{(t-1)})\frac{P(Y,Z|\theta)}{P(Z|Y,\theta^{(t-1)})}$$
    $$where  \sum_{Z}P(Z|Y,\theta^{(t-1)}) =1$$
    根据Jensen不等式，对于convex函数f(x)，有E[f(x)]>=f(E[x])。而log(x)属于concave函数，我们可以对上式放缩
    $$L(\theta|Y) \ge \sum_{Z}P(Z|Y,\theta^{(t-1)})log\frac{P(Y,Z|\theta)}{P(Z|Y,\theta^{(t-1)})}$$
    接下来我们进行M-step时，将log中的除法展开为减法，去除与$\theta$无关的常数项
    $$\theta^{(t)} = \argmax \limits_{\theta}\sum_{Z}P(Z|Y,\theta^{(t-1)})logP(Y,Z|\theta)+Constant$$
    到这里就可以看出，我们其实一直是在优化原目标的下界。若下界越大，则原目标的值也越大。通过这种方式去求解问题

 * 高斯混合模型

    高斯混合模型就是由多个高斯模型组合在一起的混合模型，例如聚类分两类时，用两个高斯模型进行划分。若要将k个高斯模型组合在一起，最简单的是线性组合
    $$P(y|\theta) = \sum_{k=1}^{K}\alpha_k\phi(y|\theta_k)\qquad where \sum_{k=1}^{K}\alpha_k =1$$
    对于第k个模型, $\theta_k\sim N(\mu_k,\sigma_k^2)$，具体表达式为
    $$\phi(y|\theta_k)=\frac{1}{\sqrt{2\pi\sigma_k^2}}exp(-\frac{(y-\mu_k)^2}{2\sigma_k^2})$$
    * 隐变量

        $\gamma_{jk}$为0-1变量表示第j个点是否来自第k个模型(第k个类)  
        此时对于某一个二维下的点i，完全数据为$((x_i,y_i),\gamma_{i1},\gamma_{i2},...,\gamma_{ik})$
    * EM算法求解

        ![GMM](GMM.jpg)
