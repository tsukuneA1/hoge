import { ExternalLink } from "lucide-react";
import { notFound } from "next/navigation";
import { Label } from "radix-ui";
import { getCourse } from "@/app/utils/api/courses";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { TypographyH1, TypographyH2 } from "@/components/ui/typography";

const EXTERNAL_BASE_URL = "https://www.wsl.waseda.jp/syllabus/JAA104.php";

type Props = {
  params: Promise<{
    pkey: string;
  }>;
};

type InfoItemProps = {
  label: string;
  content: string;
};

const CourseInfoItem = ({ label, content }: InfoItemProps) => {
  return (
    <div className="flex flex-col gap-2">
      <dt className="font-bold">{label}</dt>
      <dd>{content}</dd>
    </div>
  );
};

const SyllabusInfoItem = ({ label, content }: InfoItemProps) => {
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
      content: `${course?.campus} ${course.classroom}`,
    },
    {
      label: "授業方法区分",
      content: course.delivery_mode,
    },
    { label: "配当年次", content: course.eligible_year },
  ];

  const syllabusInfo = [
    { label: "授業概要", content: course.overview },
    { label: "授業の到達目標", content: course.objectives },
    { label: "授業計画", content: course.lesson_plan },
    { label: "教科書", content: course.textbook },
    { label: "成績評価方法", content: course.grading_policy },
    { label: "備考・関連URL", content: course.reference_text },
  ];

  return (
    <div className="flex justify-center">
      <div className="flex flex-col gap-4 max-w-5xl">
        <div className="flex gap-2 items-center">
          <TypographyH1>{course.title}</TypographyH1>
          <span>{course.instructor}</span>
          <Badge variant="default">{course.faculty}</Badge>
          <Badge variant="secondary">{course.credits}単位</Badge>
          <Button asChild>
            <a
              href={`${EXTERNAL_BASE_URL}?pKey=${course.pkey}&pLng=jp`}
              target="_blank"
              rel="noopener noreferrer"
            >
              <ExternalLink />
              公式シラバス
            </a>
          </Button>
        </div>

        <TypographyH2>授業情報</TypographyH2>
        <dl className="flex gap-4">
          {courseInfo.map((info) => {
            if (!info.content) return null;
            return (
              <CourseInfoItem
                label={info.label}
                content={info.content}
                key={info.label}
              />
            );
          })}
        </dl>

        <TypographyH2>シラバス情報</TypographyH2>

        <dl className="flex flex-col gap-2">
          {syllabusInfo.map((info) => {
            if (!info.content) return null;
            return (
              <SyllabusInfoItem
                label={info.label}
                content={info.content}
                key={info.label}
              />
            );
          })}
        </dl>
      </div>
    </div>
  );
};

export default CourseDetailPage;
