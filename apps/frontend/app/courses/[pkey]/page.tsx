import { ExternalLink } from "lucide-react";
import { getCourse } from "@/app/utils/api/courses";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { TypographyH1, TypographyH2 } from "@/components/ui/typography";
import { notFound } from "next/navigation";

type Props = {
  params: Promise<{
    pkey: string;
  }>;
};

const CourseDetailPage = async ({ params }: Props) => {
  const { pkey } = await params;

  const course = await getCourse(pkey);

  if (!course) notFound();

  return (
    <div className="flex flex-col gap-4">
      <div className="flex gap-2 items-center">
        <TypographyH1>{course?.title}</TypographyH1>
        <span>{course?.instructor}</span>
        <Badge variant="default">{course?.faculty}</Badge>
        <Badge variant="secondary">{course?.credits}単位</Badge>
        <Badge variant="secondary">{course?.delivery_mode}</Badge>
        <Button asChild>
          <a
            href={course?.source_url}
            target="_blank"
            rel="noopener noreferrer"
          >
            <ExternalLink />
            公式シラバスを見る
          </a>
        </Button>
      </div>

      <TypographyH2>授業情報</TypographyH2>
      <dl className="flex gap-4">
        <div className="flex flex-col gap-2">
          <dt className="font-bold">学期曜日時限</dt>
          <dd>{course?.term_day_period}</dd>
        </div>
        <div className="flex flex-col gap-2">
          <dt className="font-bold">科目区分</dt>
          <dd>{course?.category}</dd>
        </div>
        <div className="flex flex-col gap-2">
          <dt className="font-bold">使用教室</dt>
          <dd>
            {course?.campus}キャンパス {course?.classroom}
          </dd>
        </div>
        <div className="flex flex-col gap-2">
          <dt className="font-bold">配当年次</dt>
          <dd>{course?.eligible_year}</dd>
        </div>
      </dl>

      <TypographyH2>シラバス情報</TypographyH2>

      <dl className="flex flex-col gap-2">
        <dt className="font-bold">授業概要</dt>
        <dd>{course?.overview}</dd>
        <dt className="font-bold">授業の到達目標</dt>
        <dd>{course?.objectives}</dd>
        <dt className="font-bold">授業計画</dt>
        <dd>{course?.lesson_plan}</dd>
        <dt className="font-bold">教科書</dt>
        <dd>{course?.textbook}</dd>
        <dt className="font-bold">成績評価方法</dt>
        <dd>{course?.grading_policy}</dd>
        <dt className="font-bold">備考・関連URL</dt>
        <dd>{course?.reference_text}</dd>
      </dl>
    </div>
  );
};

export default CourseDetailPage;
