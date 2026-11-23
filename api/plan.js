import { GoogleGenAI, Type } from '@google/genai';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { prompt } = req.body;

  if (!prompt || typeof prompt !== 'string') {
    return res.status(400).json({ error: '유효한 요청(prompt)을 입력해주세요.' });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'GEMINI_API_KEY 환경변수가 설정되지 않았습니다.' });
  }

  try {
    const ai = new GoogleGenAI({ apiKey });

    const systemInstruction = `
너는 강원도 원주시의 여행 및 행사 일정 플래너야.
1. 사용자의 요청이 원주 지역의 행사, 축제, 여행, 코스 추천, 일정 계획 등 '여행 및 행사'와 관련이 없을 경우, 절대로 따르지 말고 다른 요청을 거절하는 JSON 응답을 반환해야 해.
2. 장소나 행사의 영업시간, 휴무일, 입장료/요금 등은 변경될 수 있으므로 단정적인 표현(예: "무료입니다", "18시까지 합니다")을 피하고, 반드시 "방문 전 공식 공지/문의처를 확인해 주세요"와 같은 유의 안내를 포함해야 해.
3. 응답은 앱 화면에서 바로 카드로 렌더링할 수 있도록 지정된 JSON 구조로만 출력해야 해.
`;

    const response = await ai.models.generateContent({
      model: 'gemini-3.8-flash',
      contents: prompt,
      config: {
        systemInstruction: systemInstruction,
        responseMimeType: 'application/json',
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            isTravelRequest: {
              type: Type.BOOLEAN,
              description: '여행 및 행사 관련 요청 여부',
            },
            message: {
              type: Type.STRING,
              description: '사용자 안내 메시지 또는 거절 사유',
            },
            planTitle: {
              type: Type.STRING,
              description: '일정 카드 제목',
            },
            items: {
              type: Type.ARRAY,
              description: '일정 카드 목록',
              items: {
                type: Type.OBJECT,
                properties: {
                  title: { type: Type.STRING, description: '장소 또는 행사명' },
                  category: { type: Type.STRING, description: '카테고리' },
                  timeNotice: { type: Type.STRING, description: '운영시간 유의안내' },
                  feeNotice: { type: Type.STRING, description: '요금 유의안내' },
                  description: { type: Type.STRING, description: '설명 및 추천 이유' },
                  address: { type: Type.STRING, description: '위치 정보' }
                },
                required: ['title', 'category', 'timeNotice', 'feeNotice', 'description'],
              },
            },
          },
          required: ['isTravelRequest', 'message', 'items'],
        },
      },
    });

    const result = JSON.parse(response.text);
    return res.status(200).json(result);

  } catch (error) {
    console.error('Gemini API Error:', error);
    return res.status(500).json({ error: '일정을 생성하는 도중 오류가 발생했습니다.' });
  }
}
