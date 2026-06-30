import { ExternalLink } from "lucide-react";
import { notFound } from "next/navigation";
import { getCourse } from "@/app/utils/api/courses";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { TypographyH1, TypographyH2 } from "@/components/ui/typography";

type Props = {
  params: Promise<{
    pkey: string;
  }>;
};

const CourseInfoItem = (label: string, content: string) => {
  return (
    <div className="flex flex-col gap-2" key={content}>
      <dt className="font-bold">{label}</dt>
      <dd>{content}</dd>
    </div>
  );
};

const SyllabusInfoItem = (label: string, content: string) => {
  return (
    <>
      <dt className="font-bold">{label}</dt>
      <dd className="whitespace-pre-wrap">{content}</dd>
    </>
  );
};

const CourseDetailPage = async ({ params }: Props) => {
  const { pkey } = await params;

  const course = await getCourse(pkey);

  if (!course) notFound();

  const courseInfo = [
    { label: "学期曜日時限", content: course.term_day_period },
    { label: "科目区分", content: course.category },
    {
      label: "使用教室",
      content: `${course?.campus}キャンパス ${course?.classroom}`,
    },
    { label: "配当年次", content: course.eligible_year },
  ];

  return (
    <div className="flex justify-center">
      <div className="flex flex-col gap-4 max-w-5xl">
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
          {courseInfo.map((info) => {
            if (!info.content) return;
            return CourseInfoItem(info.label, info.content);
          })}
        </dl>

        <TypographyH2>シラバス情報</TypographyH2>

        <dl className="flex flex-col gap-2">
          <dt className="font-bold">授業概要</dt>
          <dd className="whitespace-pre-wrap">{course?.overview}</dd>
          <dt className="font-bold">授業の到達目標</dt>
          <dd className="whitespace-pre-wrap">{course?.objectives}</dd>
          <dt className="font-bold">授業計画</dt>
          <dd className="whitespace-pre-wrap">{course?.lesson_plan}</dd>
          <dt className="font-bold">教科書</dt>
          <dd className="whitespace-pre-wrap">{course?.textbook}</dd>
          <dt className="font-bold">成績評価方法</dt>
          <dd className="whitespace-pre-wrap">{course?.grading_policy}</dd>
          <dt className="font-bold">備考・関連URL</dt>
          <dd className="whitespace-pre-wrap">{course?.reference_text}</dd>
        </dl>
      </div>
    </div>
  );
};

export default CourseDetailPage;
