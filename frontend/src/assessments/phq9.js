export const PHQ9 = {
  id: 'phq9',
  title: 'PHQ-9 抑郁自评量表',
  description: '请根据您过去两周的实际感受，选择最符合的选项。',
  questions: [
    {
      id: 1,
      text: '做事时提不起劲或没有兴趣',
      options: [
        { value: 0, text: '完全没有' },
        { value: 1, text: '有几天' },
        { value: 2, text: '超过一半天数' },
        { value: 3, text: '几乎每天' }
      ]
    },
    {
      id: 2,
      text: "感到心情低落、沮丧或绝望",
      options: [
        { value: 0, text: "完全不会" },
        { value: 1, text: "有几天" },
        { value: 2, text: "一半以上的天数" },
        { value: 3, text: "几乎每天" }
      ]
    },
    {
      id: 3,
      text: "入睡困难、睡不安稳或睡得太多",
      options: [
        { value: 0, text: "完全不会" },
        { value: 1, text: "有几天" },
        { value: 2, text: "一半以上的天数" },
        { value: 3, text: "几乎每天" }
      ]
    },
    {
      id: 4,
      text: "感觉疲倦或没有活力",
      options: [
        { value: 0, text: "完全不会" },
        { value: 1, text: "有几天" },
        { value: 2, text: "一半以上的天数" },
        { value: 3, text: "几乎每天" }
      ]
    },
    {
      id: 5,
      text: "食欲不振或吃太多",
      options: [
        { value: 0, text: "完全不会" },
        { value: 1, text: "有几天" },
        { value: 2, text: "一半以上的天数" },
        { value: 3, text: "几乎每天" }
      ]
    },
    {
      id: 6,
      text: "觉得自己很糟或觉得自己很失败，或让自己或家人失望",
      options: [
        { value: 0, text: "完全不会" },
        { value: 1, text: "有几天" },
        { value: 2, text: "一半以上的天数" },
        { value: 3, text: "几乎每天" }
      ]
    },
    {
      id: 7,
      text: "对事物专注有困难，例如阅读报纸或看电视时",
      options: [
        { value: 0, text: "完全不会" },
        { value: 1, text: "有几天" },
        { value: 2, text: "一半以上的天数" },
        { value: 3, text: "几乎每天" }
      ]
    },
    {
      id: 8,
      text: "行动或说话速度缓慢到别人已经察觉？或正好相反，变得比平日更烦躁或坐立不安、动来动去",
      options: [
        { value: 0, text: "完全不会" },
        { value: 1, text: "有几天" },
        { value: 2, text: "一半以上的天数" },
        { value: 3, text: "几乎每天" }
      ]
    },
    {
      id: 9,
      text: "有不如死掉或用某种方式伤害自己的念头",
      options: [
        { value: 0, text: "完全不会" },
        { value: 1, text: "有几天" },
        { value: 2, text: "一半以上的天数" },
        { value: 3, text: "几乎每天" }
      ]
    }
  ],
  scoring: {
    total: { min: 0, max: 27 },
    interpretation: [
      { range: [0, 4], level: '无抑郁', description: '您的情绪状态良好。' },
      { range: [5, 9], level: '轻度抑郁', description: '建议关注情绪变化。' },
      { range: [10, 14], level: '中度抑郁', description: '建议适当心理疏导。' },
      { range: [15, 27], level: '重度抑郁', description: '建议及时寻求专业帮助。' }
    ]
  },
  recommendations: {
    mild: [
      "保持规律的作息时间",
      "适当进行户外活动",
      "与家人朋友多交流",
      "培养兴趣爱好"
    ],
    moderate: [
      "建议咨询心理医生",
      "保持规律的作息时间",
      "适当进行户外活动",
      "与家人朋友多交流",
      "培养兴趣爱好",
      "学习放松技巧"
    ],
    severe: [
      "建议立即就医",
      "遵医嘱进行治疗",
      "保持规律的作息时间",
      "适当进行户外活动",
      "与家人朋友多交流",
      "培养兴趣爱好",
      "学习放松技巧",
      "避免独处"
    ]
  }
}; 