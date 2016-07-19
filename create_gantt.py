import gantt
import datetime

def add_bdays(from_date, add_days):
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5: # sunday = 6
            continue
        business_days_to_add -= 1
    return current_date

# Change font default
gantt.define_font_attributes(fill='black',
                             stroke='black',
                             stroke_width=0,
                             font_family="Verdana")
                             
rHGS = gantt.Resource('HGS')



book = gantt.Project('Machine Learning: Writing Schedule')

week = 5

################################
# ADJUSTABLE PARAMETERS
################################
start_date = datetime.date(2016, 9, 1)
pages_per_week = float(10)
final_review_length = 4

writing_durations = {1: [float(25) / pages_per_week, 1, 1],
                     2: [float(30) / pages_per_week, 1, 1],
                     3: [float(25) / pages_per_week, 1, 1],
                     4: [float(40) / pages_per_week, 2, 2],
                     5: [float(50) / pages_per_week, 2, 2],
                     6: [float(50) / pages_per_week, 2, 2],
                     7: [float(40) / pages_per_week, 2, 2],
                     8: [float(60) / pages_per_week, 2, 2],
                     9: [float(40) / pages_per_week, 2, 2],
                     10:[float(10) / pages_per_week, 1, 1]}


current_date = start_date
last_date = None

milestones = []
chapters = []
reviews = []
revisions = []

for current_week, duration in writing_durations.iteritems():
    chapter = gantt.Task(name = 'Chapter ' + str(current_week) + ': Writing',
                            start = current_date,
                            duration = duration[0]*week,
                            percent_done = 0,
                            color = "#2196F3")

    chapter_review = gantt.Task(name = 'Chapter ' + str(current_week) + ': Review',
                                    start = add_bdays(chapter.start,  chapter.duration),
                                    duration = duration[1]*week,
                                    depends_of = [chapter],
                                    color = "#8BC34A")

    chapter_revise = gantt.Task(name = 'Chapter ' + str(current_week) + ': Revision',
                                    start = add_bdays(chapter_review.start,   chapter_review.duration), 
                                    depends_of = [chapter_review],
                                    duration = duration[2]*week)

    milestone_chapter = gantt.Milestone(name='Complete Chapter ' + str(current_week) + '',
                                            depends_of=[chapter, chapter_review, chapter_revise])

    current_date = add_bdays(chapter.start, chapter.duration)

    chapters.append(chapter)
    reviews.append(chapter_review)
    revisions.append(chapter_revise)
    milestones.append(milestone_chapter)

    if (current_week == 1) or (add_bdays(chapter_revise.start, chapter_revise.duration) > add_bdays(last_task.start, last_task.duration)):
        last_task = chapter_revise

    book.add_task(chapter)
    book.add_task(chapter_review)
    book.add_task(chapter_revise)
    book.add_task(milestone_chapter)

milestone_book = gantt.Milestone(name = 'Complete Writing', depends_of = milestones)

current_date = add_bdays(last_task.start, last_task.duration)

final_review_author = gantt.Task(name = 'Author review',
                            start = current_date,
                            duration = final_review_length * week,
                            color = "#8BC34A")

final_review_peer = gantt.Task(name = 'Peer review',
                            start = current_date,
                            duration = final_review_length * week,
                            color = "#8BC34A")

final_revision = gantt.Task(name = 'Final Revision',
                            start = add_bdays(final_review_author.start, final_review_author.duration),
                            duration = (final_review_length / 2) * week,
                            depends_of = [final_review_author, final_review_peer])

final_submission = gantt.Milestone(name = 'Final Submission', depends_of = [final_revision])

book.add_task(milestone_book)
book.add_task(final_review_author)
book.add_task(final_review_peer)
book.add_task(final_revision)
book.add_task(final_submission)

current_chapter = 1

for chapter, review, revision in zip(chapters, reviews, revisions):
    print 'Chapter ' + str(current_chapter)
    print '\tStart: ' + str(chapter.start)
    print '\tWriting Duration (Weeks): ' + str(chapter.duration / week)
    print '\tReview/Revision Duration (Weeks): ' + str((review.duration + revision.duration) / week)
    print '\tCompletion: ' + str(add_bdays(revision.start, revision.duration))


    current_chapter += 1


print '--'
print 'Wrap-up: '
print '\tStart: ' + str(current_date)
print '\tReview Duration (Weeks): ' + str(final_review_author.duration / week)
print '\tRevision Duration (Weeks): ' + str(final_revision.duration / week)
print '\tCompletion: ' + str(add_bdays(final_revision.start, final_revision.duration))
print '--'

print 'Total Duration: ' + str(add_bdays(final_revision.start, final_revision.duration) - start_date)

book.make_svg_for_tasks(filename='writing_schedule_hgs.svg',
                     today=datetime.date(2016, 7, 18),
                     start=start_date,
                     end=add_bdays(final_revision.start, final_revision.duration + week))