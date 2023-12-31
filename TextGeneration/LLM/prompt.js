export const throw_type = [
    "拉引击石：将冰壶石掷在得分区之前或得分区内。",
    "防卫击石：将冰壶石掷在拱线和得分区之间用来防御对手的冰壶石进入得分区。",
    "敲退击石：将冰壶石放在一个或是多个已经存在场上的冰壶石的前面。",
    "通道击石：当掷石者需要让他的冰壶石通过两颗或是多阻碍石时，他便需要掷出一个ports shot。",
    "晋升击石：将一颗在得分区之前的冰壶石，由射石撞击到更接近得分区的中心",
    "晋升移除掷石：一颗冰壶石被射石撞击之后，往后推近并碰击到对方的冰壶石，而使对方的石冰壶石被驱离得分区或出局的射击。",
    "精彩击石：若希望将冰壶石掷到一颗卫兵石的后面；或是希望将一颗被保护的很好的冰壶石击出场，有一种方式是将冰壶石丢掷去撞击一颗停在外围的冰壶石，然后让掷石转向朝目标地方向前进。",
    "冰壶的技术/战术其实就是投掷、引导和擦冰，三者都是默契配合的，不同的战术决定不同的投掷方式和力度，不同的战术也决定不同的擦冰方式和速度。",
].join("\n");

export const layout_type = [
    "中心控制型布局：中心控制型布局是最常见的一种布局方式。在这种布局下，进攻方会在中心区域形成一个抢中心点的态势。此时，防守方可以采取封锁中心的策略，或者通过中心反击来打破对手的进攻。",
    "边控型布局：边控型布局是以控制两条侧边为主要目标的一种布局方式。在这种布局下，进攻方会在侧边投掷石头，并且尽可能地将石头靠近底线，以此来控制场上的空间和节奏。防守方需要有效地防守两条侧边，以防止对手得分。",
    "翻转型布局：翻转型布局是一种比较具有变化性的布局方式。在这种布局下，进攻方会用一些假动作来引导防守方的注意力，然后突然改变方向，从另一个方向展开进攻。这种布局方式需要进攻方有较高的技巧和配合默契度。",
    "散打型布局：散打型布局是一种相对自由的布局方式。在这种布局下，进攻方不会固定投掷石头的位置，而是根据对手的防守情况进行自由选择。这种布局方式一般需要进攻方具备较强的判断能力和技巧水平。",
].join("\n");

export const prompt = `以下是一些冰壶的投石方式：
${throw_type}

以下是一些冰壶的布局方式：
${layout_type}

请你根据场上冰壶坐标分析局势，请勿重复场上的局势，请不要给出冰壶坐标，直接给出你的判断，这场上的局势，所有数据单位都是米：
`;

export const pos2nl = (x, y, c) => `有一个${c}壶位于(${x}, ${y})处\n`;